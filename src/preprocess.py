import argparse
import html
import re
import string
from pathlib import Path

import pandas as pd


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
    "this",
    "these",
    "those",
    "or",
    "not",
    "can",
    "we",
    "our",
    "their",
    "using",
    "use",
    "used",
    "into",
    "than",
    "also",
    "such",
    "between",
    "within",
    "through",
    "based",
}


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = [token for token in text.split() if token not in STOPWORDS and len(token) > 2]
    return " ".join(tokens)


def preprocess_dataframe(df: pd.DataFrame, min_clean_tokens: int = 10) -> pd.DataFrame:
    required_cols = {"record_id", "title", "abstract_text", "journal_name", "pub_year"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    output = df.copy()
    output["title"] = output["title"].fillna("").astype(str).str.strip()
    output["abstract_text"] = output["abstract_text"].fillna("").astype(str).str.strip()
    output["journal_name"] = output["journal_name"].fillna("").astype(str).str.strip()

    output = output[
        (output["title"] != "")
        & (output["abstract_text"] != "")
        & (output["journal_name"] != "")
    ].copy()

    output["abstract_clean"] = output["abstract_text"].apply(clean_text)
    output["clean_token_count"] = output["abstract_clean"].str.split().str.len()

    output = output[output["clean_token_count"] >= min_clean_tokens].copy()
    output = output.sort_values("record_id").reset_index(drop=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess article dataset for journal recommendation.")
    parser.add_argument("--input", default="outputs/base_articles.csv", help="Path to raw CSV.")
    parser.add_argument("--output", default="outputs/base_articles_clean.csv", help="Path to cleaned CSV.")
    parser.add_argument(
        "--min-clean-tokens",
        type=int,
        default=10,
        help="Minimum token count required after cleaning.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    cleaned = preprocess_dataframe(df, min_clean_tokens=args.min_clean_tokens)
    cleaned.to_csv(output_path, index=False)

    print(f"Input rows:   {len(df)}")
    print(f"Output rows:  {len(cleaned)}")
    print(f"Saved to:     {output_path}")


if __name__ == "__main__":
    main()
