# Data Mining Final Project

This repository contains a journal finder project built from the instructor-provided computer science publication database.

## Deliverables Covered

- Source code
- Jupyter notebook
- IEEE-style report draft
- Working top-5 journal recommender
- Topic clustering output

## Project Structure

- `CompSciencePub.sqlite`: instructor-provided SQLite database
- `CS_JournalAbstracts.zip`: instructor-provided database backup archive
- `src/extract_cs_dataset.sql`: SQL query to build the CS article dataset
- `src/preprocess.py`: preprocessing and feature-text generation
- `src/recommender.py`: TF-IDF journal recommendation script
- `src/evaluation.py`: Hit@5 evaluation script
- `src/clustering.py`: topic clustering script
- `notebooks/journal_finder.ipynb`: demonstration notebook
- `report/ieee_report.md`: report draft
- `outputs/`: generated CSV files

## Setup

Install requirements:

```bash
python3 -m pip install pandas scikit-learn notebook
```

## Usage

### 1. Extract the CS article dataset

```bash
mkdir -p outputs
sqlite3 "CompSciencePub.sqlite" \
  -cmd ".headers on" \
  -cmd ".mode csv" \
  -cmd ".output outputs/base_articles.csv" \
  < "src/extract_cs_dataset.sql"
```

### 2. Preprocess the dataset

```bash
python3 src/preprocess.py \
  --input outputs/base_articles.csv \
  --output outputs/base_articles_clean.csv
```

### 3. Run a journal recommendation query

```bash
python3 src/recommender.py \
  --input outputs/base_articles_clean.csv \
  --query "This paper proposes a machine learning intrusion detection framework for cloud computing environments."
```

### 4. Evaluate the recommender

```bash
python3 src/evaluation.py \
  --input outputs/base_articles_clean.csv \
  --sample-size 300 \
  --k 5
```

### 5. Generate topic clusters

```bash
python3 src/clustering.py \
  --input outputs/base_articles_clean.csv \
  --k 8 \
  --output outputs/topic_clusters.csv
```

## Notes

- The extraction query is constrained to a `175 journal / 7711 article` subset so the working dataset matches the assignment statement.
- The subset uses computer-science-tagged articles and a transparent journal selection rule encoded in [extract_cs_dataset.sql](/Users/sametbilgin/Desktop/data-term/src/extract_cs_dataset.sql).
- The recommendation baseline uses TF-IDF plus cosine similarity.
- Topic clustering uses KMeans on TF-IDF representations of article text, subjects, and keywords.
