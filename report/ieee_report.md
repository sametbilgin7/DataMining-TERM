# Journal Finder for Computer Science Articles

## Abstract
Selecting the most suitable journal for a new manuscript is a difficult and time-consuming task for researchers. In this project, we develop a journal recommendation system for computer science publications using article abstracts. The proposed method uses a TF-IDF vector space representation and cosine similarity to retrieve semantically similar articles and rank candidate journals. In addition, we perform topic clustering on abstracts to reveal major thematic groups in the dataset. Experiments on the provided publication database show that the model can return relevant journals in top-5 recommendations with promising performance. The final system supports an input abstract and outputs the top-5 most relevant journals.

## 1. Introduction
Journal selection has a direct impact on publication success, visibility, and citation potential. Researchers often spend significant effort to identify journals aligned with the manuscript scope and quality. This process is especially difficult in computer science due to diverse subfields and a large number of venues.

In this work, we design a data-driven journal finder system using historical publication metadata and abstracts. Given a query abstract, the system recommends the five most relevant journals. We also cluster article abstracts to identify dominant research themes in the dataset.

## 2. Related Work
Text-based recommendation approaches are widely used in information retrieval and scholarly systems. Classical methods represent documents with bag-of-words or TF-IDF features and compute similarity using cosine distance. More recent approaches include topic models and neural embeddings. For transparent and reproducible baseline performance in this course project, we adopt a TF-IDF + cosine framework and complement it with clustering analysis.

## 3. Dataset and Preprocessing
### 3.1 Data Source
The project uses the provided `CompSciencePub.sqlite` database. Core tables used in this study:

- `AcademicRecord` (article metadata)
- `AcademicRecordAbstract` (abstract text)
- `Publication` (journal names)

After joining and filtering, the base dataset contains article id, title, abstract, journal name, and publication year.

### 3.2 Data Preparation
Preprocessing steps:

1. Remove records with missing title, abstract, or journal name.
2. Clean HTML tags from abstract text.
3. Lowercase normalization.
4. Remove punctuation and numeric tokens.
5. Remove common stopwords.
6. Remove very short cleaned texts (token threshold).

The resulting cleaned field (`abstract_clean`) is used for model training and inference.

## 4. Methodology
### 4.1 Journal Recommendation
We represent each article abstract as a TF-IDF vector using uni-grams and bi-grams. For a new query abstract:

1. Transform query text into the same TF-IDF space.
2. Compute cosine similarity to all training abstracts.
3. Select top similar documents.
4. Aggregate similarity scores by journal.
5. Return top-5 journals by total score.

This method is simple, interpretable, and effective as a baseline recommender.

### 4.2 Topic Clustering
To discover thematic structure in the corpus, we apply clustering (e.g., KMeans) on vectorized abstracts. Cluster labels are interpreted using top weighted terms and dominant journals per cluster.

## 5. Experimental Setup
- Train/test split: 80/20 random split.
- Recommendation metric: `Hit@5` (whether true journal appears in top-5).
- Additional qualitative inspection: top recommended journals for custom query abstracts.

Implementation environment:
- Python 3
- pandas
- scikit-learn
- SQLite as data backend

## 6. Results
### 6.1 Recommendation Output Example
For a sample abstract on machine learning-based intrusion detection in cloud environments, the system recommends journals such as:

1. JOURNAL OF NETWORK AND COMPUTER APPLICATIONS
2. COMPUTERS & SECURITY
3. COMPUTERS & ELECTRICAL ENGINEERING
4. JOURNAL OF MACHINE LEARNING RESEARCH
5. COMPUTER SYSTEMS SCIENCE AND ENGINEERING

These results are semantically consistent with cybersecurity and ML themes.

### 6.2 Quantitative Evaluation
`Hit@5` is computed on a sampled test subset in the notebook.  
Measured result:

- Hit@5 (sample=200): `0.5550`
- (Optional) Full-test Hit@5: `not computed yet`

### 6.3 Topic Clustering Summary
KMeans clustering was applied with `k=8` on TF-IDF vectors of cleaned abstracts. The silhouette score was `0.0031`, indicating overlapping topic boundaries in this broad corpus. Despite the low silhouette value, clusters remain interpretable via top terms:

- Cluster (data-centric): `data, mining, big, clustering, big data`
- Cluster (cloud/services): `cloud, service, services, computing, cloud computing`
- Cluster (networks): `network, networks, sensor, wireless, routing`
- Cluster (vision/ML): `image, classification, recognition, features, learning`
- Cluster (optimization): `algorithm, problem, optimization, search, solution`

## 7. Discussion
Strengths:
- Transparent and easy-to-explain recommendation logic.
- Fast retrieval for practical usage.
- Good baseline quality with limited engineering overhead.

Limitations:
- Vocabulary mismatch for novel terminology.
- Popular journals may dominate score aggregation.
- No citation network or author-level features used.

Potential improvements:
- BM25 or transformer embeddings.
- Journal-level calibration and re-ranking.
- Hybrid approach combining subject/keyword metadata.

## 8. Conclusion
This project demonstrates a practical journal finder system for computer science abstracts. The TF-IDF + cosine approach provides interpretable top-5 journal recommendations and forms a solid baseline for further improvement. Topic clustering adds an additional analytical layer by revealing high-level research themes. The developed pipeline can be extended with advanced language models and richer metadata for improved recommendation accuracy.

## References
[1] C. D. Manning, P. Raghavan, and H. Schutze, *Introduction to Information Retrieval*. Cambridge University Press, 2008.  
[2] G. Salton and C. Buckley, "Term-weighting approaches in automatic text retrieval," *Information Processing & Management*, vol. 24, no. 5, pp. 513-523, 1988.  
[3] T. Mikolov et al., "Distributed representations of words and phrases and their compositionality," *NeurIPS*, 2013.  
[4] J. Devlin et al., "BERT: Pre-training of deep bidirectional transformers for language understanding," *NAACL-HLT*, 2019.

