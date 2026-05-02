WITH subject_agg AS (
  SELECT
    ars.AcademicRecordId AS record_id,
    group_concat(DISTINCT s.NameEn) AS subject_terms
  FROM AcademicRecordSubject ars
  JOIN AcademicSubject s
    ON s.AcademicSubjectID = ars.AcademicSubjectId
  GROUP BY ars.AcademicRecordId
),
keyword_agg AS (
  SELECT
    ark.AcademicRecordId AS record_id,
    group_concat(DISTINCT ak.Name) AS keyword_terms
  FROM AcademicRecordKeyword ark
  JOIN AcademicKeyword ak
    ON ak.AcademicKeywordID = ark.AcademicKeywordId
  GROUP BY ark.AcademicRecordId
),
keyword_plus_agg AS (
  SELECT
    arkp.AcademicRecordId AS record_id,
    group_concat(DISTINCT akp.Name) AS keyword_plus_terms
  FROM AcademicRecordKeywordPlus arkp
  JOIN AcademicKeywordPlus akp
    ON akp.AcademicKeywordPlusID = arkp.AcademicKeywordPlusId
  GROUP BY arkp.AcademicRecordId
)
SELECT
  ar.AcademicRecordID AS record_id,
  ar.Title AS title,
  ara.AbstractText AS abstract_text,
  p.Name AS journal_name,
  ar.PubYear AS pub_year,
  sa.subject_terms,
  ka.keyword_terms,
  kpa.keyword_plus_terms
FROM AcademicRecord ar
JOIN AcademicRecordAbstract ara
  ON ara.AcademicRecordId = ar.AcademicRecordID
JOIN Publication p
  ON p.PublicationID = ar.PublicationId
LEFT JOIN DocumentType dt
  ON dt.DocumentTypeID = ar.DocumentTypeId
LEFT JOIN subject_agg sa
  ON sa.record_id = ar.AcademicRecordID
LEFT JOIN keyword_agg ka
  ON ka.record_id = ar.AcademicRecordID
LEFT JOIN keyword_plus_agg kpa
  ON kpa.record_id = ar.AcademicRecordID
WHERE ara.AbstractText IS NOT NULL
  AND trim(ara.AbstractText) <> ''
  AND ar.Title IS NOT NULL
  AND trim(ar.Title) <> ''
  AND p.Name IS NOT NULL
  AND trim(p.Name) <> ''
  AND dt.NameEn = 'Article'
  AND EXISTS (
    SELECT 1
    FROM AcademicRecordSubject ars2
    JOIN AcademicSubject s2
      ON s2.AcademicSubjectID = ars2.AcademicSubjectId
    WHERE ars2.AcademicRecordId = ar.AcademicRecordID
      AND (s2.NameEn = 'Computer Science' OR s2.NameEn LIKE 'Computer Science,%')
  )
  AND (
    p.Name LIKE '%COMPUTER%'
    OR p.Name LIKE '%COMPUTING%'
    OR p.Name LIKE '%COMPUTATIONAL%'
    OR p.Name IN (
      'KNOWLEDGE AND INFORMATION SYSTEMS',
      'IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS',
      'INTERNATIONAL JOURNAL OF SOFTWARE ENGINEERING AND KNOWLEDGE ENGINEERING',
      'NEURAL NETWORKS',
      'INFORMATION AND SOFTWARE TECHNOLOGY',
      'WORLD WIDE WEB-INTERNET AND WEB INFORMATION SYSTEMS',
      'NEURAL NETWORK WORLD',
      'INTERNATIONAL JOURNAL OF INFORMATION SECURITY',
      'JOURNAL OF INFORMATION SECURITY AND APPLICATIONS',
      'JOURNAL OF LOGIC LANGUAGE AND INFORMATION',
      'JOURNAL OF THE ASSOCIATION FOR INFORMATION SYSTEMS'
    )
  )
ORDER BY ar.AcademicRecordID;
