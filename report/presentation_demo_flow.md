# 5-7 Minute Demo Flow

## 0:00-0:40 - Problem and Goal
- Explain the pain point: choosing the right journal is hard and time-consuming.
- State project goal: input abstract -> output top-5 relevant journals.
- Mention dataset source: `CompSciencePub.sqlite` (computer science publication records).

## 0:40-1:40 - Data and Pipeline
- Show core tables used: `AcademicRecord`, `AcademicRecordAbstract`, `Publication`.
- Explain preprocessing briefly:
  - remove missing abstract/title/journal rows
  - HTML cleanup
  - lowercase + punctuation/number cleanup
  - stopword filtering
- Mention produced files:
  - `outputs/base_articles.csv`
  - `outputs/base_articles_clean.csv`

## 1:40-3:10 - Recommendation Method
- Explain model in one sentence: TF-IDF vectors + cosine similarity.
- Explain ranking logic:
  1. compare query abstract with all document abstracts
  2. take top similar documents
  3. aggregate similarity by journal
  4. return top 5 journals
- Open `notebooks/journal_finder.ipynb` and run the sample query cell.

## 3:10-4:20 - Quantitative Result
- Show metric cell output:
  - `Hit@5 (sample=200) = 0.5550`
- Interpret simply:
  - in ~55.5% of sampled test cases, the true journal appears in top-5 recommendations.
- Mention this is a baseline and can be improved with richer models.

## 4:20-5:40 - Topic Clustering Result
- Show `src/clustering.py` output summary.
- Mention:
  - KMeans with `k=8`
  - silhouette: `0.0053`
- Explain key clusters (examples):
  - cloud/services
  - wireless sensor networks
  - image/vision
  - optimization/algorithms

## 5:40-6:30 - Limitations and Improvements
- Limitations:
  - lexical mismatch for unseen terms
  - skew toward frequent journals
  - no citation/author features
- Next steps:
  - BM25 baseline
  - sentence embeddings
  - metadata-enhanced hybrid ranking

## 6:30-7:00 - Closing
- Restate deliverable success:
  - working top-5 journal recommender
  - notebook + report + code repository
- Invite questions and be ready to run one extra custom abstract live.
