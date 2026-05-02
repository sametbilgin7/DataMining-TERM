# 5-7 Minute Demo Flow

## 0:00-0:40 - Problem
- Journal selection is difficult for researchers.
- The project goal is: input an abstract, return the top 5 relevant journals.
- The assignment also requires topic clustering.

## 0:40-1:30 - Dataset
- Mention the instructor-provided database.
- State the working subset used in the project: `7711 articles` from `175 journals`.
- Show the main tables:
  - `AcademicRecord`
  - `AcademicRecordAbstract`
  - `Publication`
  - `AcademicRecordSubject`
  - `AcademicRecordKeyword`
  - `AcademicRecordKeywordPlus`

## 1:30-2:30 - Pipeline
- Explain the extraction query.
- Explain preprocessing:
  - HTML cleanup
  - lowercasing
  - punctuation/number removal
  - stopword removal
  - combined feature text from abstract + subject + keywords

## 2:30-3:40 - Recommendation
- Explain TF-IDF + cosine similarity.
- Explain that similar articles are found first, then scores are aggregated by journal.
- Show the sample query in the notebook.
- Show the top-5 recommended journals.

## 3:40-4:20 - Evaluation
- Show `Hit@5 (sample=300) = 0.6667`.
- Explain the meaning: the correct journal appears in the top-5 list about 67% of the time on the sampled test set.

## 4:20-5:20 - Clustering
- Show the cluster output.
- Mention `k=8`.
- Mention silhouette score `0.0032`.
- Explain a few interpretable clusters:
  - software/systems
  - cloud/performance
  - wireless sensor networks
  - optimization
  - neural/data-driven learning

## 5:20-6:00 - Close
- Restate that all required deliverables are prepared:
  - code
  - notebook
  - report
  - working journal finder
  - topic clustering
