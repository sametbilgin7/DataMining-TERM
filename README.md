# DataMining-TERM: Journal Finder Project

This repository contains a data mining project that recommends the top-5 journals for a given computer science abstract.

## Project Structure

- `CompSciencePub.sqlite`: main dataset (SQLite)
- `CS_JournalAbstracts.zip`: backup archive (`CompSciencePub.bak`)
- `src/extract_base_dataset.sql`: SQL query to build base dataset
- `src/preprocess.py`: preprocessing pipeline for text cleaning
- `src/recommender.py`: TF-IDF + cosine based top-5 journal recommender
- `notebooks/journal_finder.ipynb`: notebook for demo and evaluation
- `report/ieee_report.md`: IEEE-style report draft
- `outputs/`: generated CSV files

## Requirements

- Python 3.9+
- SQLite (`sqlite3`)
- Python packages:
  - `pandas`
  - `scikit-learn`

Install packages:

```bash
python3 -m pip install pandas scikit-learn
```

## Step-by-Step Usage

### 1) Build base dataset from SQLite

```bash
cd "/Users/sametbilgin/Desktop/data-term"
sqlite3 "CompSciencePub.sqlite" \
  -cmd ".headers on" \
  -cmd ".mode csv" \
  -cmd ".output outputs/base_articles.csv" \
  < "src/extract_base_dataset.sql"
```

Expected output file:
- `outputs/base_articles.csv`

### 2) Preprocess and clean text

```bash
python3 "src/preprocess.py" \
  --input "outputs/base_articles.csv" \
  --output "outputs/base_articles_clean.csv"
```

Expected output file:
- `outputs/base_articles_clean.csv`

### 3) Run journal recommendation

```bash
python3 "src/recommender.py" \
  --input "outputs/base_articles_clean.csv" \
  --query "This study proposes a machine learning based intrusion detection framework for cloud computing environments using feature selection and ensemble classification." \
  --top-k 5
```

The command returns:
- ranked top-5 journal names
- aggregated similarity scores
- matched document counts

### 4) Open notebook for demonstration

Open and run:
- `notebooks/journal_finder.ipynb`

Notebook includes:
- data loading and quick EDA
- model building
- sample recommendation output
- simple `Hit@5` evaluation

## Deliverables Checklist

- [x] Source code in GitHub repository
- [x] Jupyter notebook
- [x] IEEE-style report draft
- [x] Working top-5 journal recommender
- [ ] Final report PDF export
- [ ] Final metric values filled in report

## Notes

- `CompSciencePub.sqlite` is a large file and may trigger GitHub large-file warnings.
- Consider adding `.gitignore` for system files (for example `.DS_Store`) before final cleanup commit.
