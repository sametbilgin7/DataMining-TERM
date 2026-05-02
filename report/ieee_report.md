# Journal Finder for Computer Science Articles

## Abstract
Choosing the right journal for a manuscript is a difficult decision for researchers because journals differ in scope, audience, and impact. This project develops a journal finder system for computer science articles by using the instructor-provided publication database. The method combines article abstracts with subject labels and keyword metadata, builds a TF-IDF representation, and ranks journals by cosine similarity. In addition, topic clustering is applied to reveal broad subject-area structure in the corpus. The final system accepts an input abstract and returns the top five most relevant journals.

## 1. Introduction
Journal selection is an important step in the publication workflow. A poor journal choice can reduce the probability of acceptance and delay the publication process. In computer science, the diversity of subfields makes venue selection especially challenging. Researchers working in artificial intelligence, software engineering, information systems, computer networks, theory, and interdisciplinary areas often need support in matching their work with appropriate journals.

The objective of this course project is to build a data mining pipeline that recommends candidate journals from past publication data. The assignment also requires clustering of topic areas in the dataset. Therefore, this project includes two outputs: a top-5 journal recommendation system and a topic clustering analysis over the same article collection.

## 2. Related Work
Text-based recommendation systems commonly represent documents with sparse lexical features such as bag-of-words, TF-IDF, or BM25. These methods remain useful because they are interpretable, efficient, and straightforward to evaluate. In information retrieval, cosine similarity over TF-IDF vectors is a standard baseline for ranking related documents and has strong practical performance for domain-specific corpora.

Topic discovery in document collections is often performed with unsupervised learning methods such as clustering or topic modeling. KMeans over TF-IDF vectors provides a simple and reproducible approach for grouping documents with similar vocabulary. Although cluster quality can be sensitive to broad and overlapping subject areas, the resulting top terms still provide useful thematic summaries.

Recent journal recommendation systems may combine semantic embeddings, citation links, author features, or journal metadata. However, a transparent lexical baseline is suitable for a course project because it demonstrates the full pipeline from data preparation to evaluation and can be extended later.

## 3. Dataset and Feature Construction
The project uses the provided `CompSciencePub.sqlite` database. The assignment description states that the material covers `7711` articles from `175` computer science journals. The extraction query therefore enforces a `175`-journal subset and keeps only article records with non-empty titles and abstracts and at least one `Computer Science` subject label.

The following entities are used:

- `AcademicRecord`
- `AcademicRecordAbstract`
- `Publication`
- `AcademicRecordSubject`
- `AcademicRecordKeyword`
- `AcademicRecordKeywordPlus`

For each article, the extracted fields are:

- record id
- title
- abstract text
- journal name
- publication year
- aggregated subject terms
- aggregated author keywords
- aggregated keyword-plus terms

The model text is built by combining cleaned title, abstract, subject labels, author keywords, and keyword-plus terms. The abstract is given extra weight by repeating it once in the combined text.

## 4. Methodology
### 4.1 Journal Recommendation
The recommendation pipeline follows these steps:

1. Clean and normalize text by removing HTML tags, punctuation, numbers, and common stopwords.
2. Convert each article to a TF-IDF vector using unigrams and bigrams.
3. Transform the query abstract into the same vector space.
4. Compute cosine similarity between the query and all training articles.
5. Select the most similar articles and aggregate their similarity scores by journal.
6. Return the top five journals with the highest aggregated scores.

This approach is interpretable because the recommendation is based on textual similarity to previously published articles.

### 4.2 Topic Clustering
The clustering pipeline uses the same cleaned model text. TF-IDF vectors are built and then clustered with KMeans. Each cluster is interpreted by examining the highest-weighted terms in the centroid. This provides a compact summary of major themes within the computer science article collection.

## 5. Experimental Setup
The implementation uses:

- Python 3
- pandas
- scikit-learn
- SQLite

Evaluation for the recommender is performed with a train/test split and the `Hit@5` metric. A prediction is counted as a hit if the correct journal of the test article appears in the returned top-5 list.

## 6. Results
After filtering to the assignment-aligned subset, the extracted working dataset contains exactly `7,711` articles from `175` journals. After preprocessing, `7,694` articles remain.

### 6.1 Recommendation Example
For the sample abstract about machine learning based intrusion detection in cloud environments, the recommender returns:

1. `COMPUTERS & SECURITY`
2. `COMPUTERS & ELECTRICAL ENGINEERING`
3. `KNOWLEDGE AND INFORMATION SYSTEMS`
4. `COMPUTER SYSTEMS SCIENCE AND ENGINEERING`
5. `NEUROCOMPUTING`

These journals are consistent with themes of cybersecurity, systems, and data-driven analysis.

### 6.2 Quantitative Evaluation
Using a random train/test split and `Hit@5` evaluation on a sample of `300` test articles, the measured score is:

- `Hit@5 = 0.6667`

This means that the correct journal appears in the top-5 recommendation list for roughly 67% of sampled test articles.

### 6.3 Topic Clustering
KMeans clustering with `k=8` gives a silhouette score of `0.0032`. The low score suggests overlapping topic boundaries, which is expected in a broad computer science corpus. Even so, the clusters remain interpretable:

- software engineering and systems development
- numerical and model-based methods
- cloud computing and performance
- information systems, security, and users
- wireless and sensor networks
- optimization, search, and metaheuristics
- neural/data-driven learning
- theory, graphs, and logic

Representative top terms include:

- Cluster 0: `software, systems, design, development, paper`
- Cluster 2: `performance, computing, cloud, data, applications`
- Cluster 4: `sensor, wireless, networks, sensor networks, wireless sensor`
- Cluster 6: `neural, data, method, proposed, using`

## 7. Discussion
The approach has several strengths:

- simple and reproducible pipeline
- interpretable recommendation logic
- ability to incorporate metadata as text features
- direct mapping from abstract input to journal output

The main limitations are:

- lexical mismatch for semantically similar but differently worded abstracts
- possible bias toward journals with more training examples
- overlap between broad computer science subject areas

Future improvements could include BM25 ranking, sentence embeddings, hybrid metadata features, or journal-level re-ranking.

## 8. Conclusion
This project builds a complete baseline journal finder for computer science articles using the provided database. The final deliverable includes a top-5 recommendation system, topic clustering analysis, notebook demonstration, and report. The pipeline is intentionally simple, transparent, and suitable for extension with stronger retrieval models.

## References
[1] C. D. Manning, P. Raghavan, and H. Schutze, *Introduction to Information Retrieval*. Cambridge University Press, 2008.  
[2] G. Salton and C. Buckley, "Term-weighting approaches in automatic text retrieval," *Information Processing & Management*, vol. 24, no. 5, pp. 513-523, 1988.  
[3] K. Sparck Jones, "A statistical interpretation of term specificity and its application in retrieval," *Journal of Documentation*, vol. 28, no. 1, pp. 11-21, 1972.  
[4] J. MacQueen, "Some methods for classification and analysis of multivariate observations," in *Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability*, 1967, pp. 281-297.  
[5] S. Robertson and H. Zaragoza, "The probabilistic relevance framework: BM25 and beyond," *Foundations and Trends in Information Retrieval*, vol. 3, no. 4, pp. 333-389, 2009.
