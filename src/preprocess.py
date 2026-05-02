import argparse
import html
import re
import string
from pathlib import Path

import pandas as pd


STOPWORDS = {
    "a",
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "also",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "he",
    "her",
    "here",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "itself",
    "just",
    "me",
    "more",
    "most",
    "my",
    "myself",
    "no",
    "nor",
    "not",
    "now",
    "of",
    "off",
    "on",
    "once",
    "only",
    "or",
    "other",
    "our",
    "ours",
    "ourselves",
    "out",
    "over",
    "own",
    "same",
    "she",
    "should",
    "so",
    "some",
    "such",
    "than",
    "that",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "whom",
    "why",
    "with",
    "would",
    "rights",
    "reserved",
    "elsevier",
    "ltd",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
}


BOILERPLATE_PATTERNS = [
    r"\(c\)\s*\d{4}[^.]*all rights reserved\.?",
    r"copyright\s*\d{4}[^.]*all rights reserved\.?",
    r"published by elsevier[^.]*\.?",
    r"elsevier science ltd[^.]*\.?",
    r"all rights reserved\.?",
]


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    for pattern in BOILERPLATE_PATTERNS:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)
    text = text.lower()
    text = text.replace("&", " and ")
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = [token for token in text.split() if token not in STOPWORDS and len(token) > 2]
    return " ".join(tokens)


def build_model_text(row: pd.Series) -> str:
    parts = [
        row.get("title_clean", ""),
        row.get("abstract_clean", ""),
        row.get("abstract_clean", ""),
        row.get("subject_terms_clean", ""),
        row.get("keyword_terms_clean", ""),
        row.get("keyword_plus_terms_clean", ""),
    ]
    return " ".join(part for part in parts if part).strip()


def preprocess_dataframe(df: pd.DataFrame, min_clean_tokens: int = 15) -> pd.DataFrame:
    required_cols = {
        "record_id",
        "title",
        "abstract_text",
        "journal_name",
        "pub_year",
        "subject_terms",
        "keyword_terms",
        "keyword_plus_terms",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    work = df.copy()
    for col in required_cols:
        work[col] = work[col].fillna("").astype(str).str.strip()

    work = work[(work["title"] != "") & (work["abstract_text"] != "") & (work["journal_name"] != "")].copy()

    work["title_clean"] = work["title"].apply(clean_text)
    work["abstract_clean"] = work["abstract_text"].apply(clean_text)
    work["subject_terms_clean"] = work["subject_terms"].apply(clean_text)
    work["keyword_terms_clean"] = work["keyword_terms"].apply(clean_text)
    work["keyword_plus_terms_clean"] = work["keyword_plus_terms"].apply(clean_text)
    work["clean_token_count"] = work["abstract_clean"].str.split().str.len()
    work = work[work["clean_token_count"] >= min_clean_tokens].copy()

    work["model_text"] = work.apply(build_model_text, axis=1)
    work["model_token_count"] = work["model_text"].str.split().str.len()
    work = work[work["model_token_count"] >= min_clean_tokens].copy()

    work["pub_year"] = pd.to_numeric(work["pub_year"], errors="coerce")
    work = work.sort_values(["journal_name", "pub_year", "record_id"]).reset_index(drop=True)
    return work


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess the CS journal article dataset.")
    parser.add_argument("--input", default="outputs/base_articles.csv", help="Input CSV path.")
    parser.add_argument("--output", default="outputs/base_articles_clean.csv", help="Output CSV path.")
    parser.add_argument("--min-clean-tokens", type=int, default=15, help="Minimum cleaned abstract token count.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    cleaned = preprocess_dataframe(df, min_clean_tokens=args.min_clean_tokens)
    cleaned.to_csv(output_path, index=False)

    print(f"Input rows: {len(df)}")
    print(f"Output rows: {len(cleaned)}")
    print(f"Unique journals: {cleaned['journal_name'].nunique()}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
