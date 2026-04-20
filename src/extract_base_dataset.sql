SELECT
  ar.AcademicRecordID AS record_id,
  ar.Title AS title,
  ara.AbstractText AS abstract_text,
  p.Name AS journal_name,
  ar.PubYear AS pub_year
FROM AcademicRecord ar
INNER JOIN AcademicRecordAbstract ara
  ON ara.AcademicRecordId = ar.AcademicRecordID
INNER JOIN Publication p
  ON p.PublicationID = ar.PublicationId
WHERE ara.AbstractText IS NOT NULL
  AND trim(ara.AbstractText) <> ''
  AND ar.Title IS NOT NULL
  AND trim(ar.Title) <> ''
  AND p.Name IS NOT NULL
  AND trim(p.Name) <> '';
