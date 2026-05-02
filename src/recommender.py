import argparse
from dataclasses import dataclass

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from preprocess import clean_text


@dataclass
class JournalRecommender:
    vectorizer: TfidfVectorizer
    doc_matrix: any
    journals: pd.Series
    titles: pd.Series
    years: pd.Series

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        text_col: str = "model_text",
        journal_col: str = "journal_name",
        max_features: int = 50000,
        ngram_range: tuple = (1, 2),
        min_df: int = 3,
        max_df: float = 0.9,
    ) -> "JournalRecommender":
        required_cols = {text_col, journal_col, "title", "pub_year"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"DataFrame must contain columns: {sorted(required_cols)}")

        work = df[list(required_cols)].dropna().copy()
        work[text_col] = work[text_col].astype(str).str.strip()
        work[journal_col] = work[journal_col].astype(str).str.strip()
        work["title"] = work["title"].astype(str).str.strip()
        work = work[(work[text_col] != "") & (work[journal_col] != "")]

        vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            norm="l2",
            sublinear_tf=True,
        )
        doc_matrix = vectorizer.fit_transform(work[text_col])
        return cls(
            vectorizer=vectorizer,
            doc_matrix=doc_matrix,
            journals=work[journal_col].reset_index(drop=True),
            titles=work["title"].reset_index(drop=True),
            years=work["pub_year"].reset_index(drop=True),
        )

    def recommend(self, query_abstract: str, top_k: int = 5, candidate_pool: int = 300) -> list[dict]:
        if not isinstance(query_abstract, str) or not query_abstract.strip():
            raise ValueError("query_abstract must be a non-empty string.")

        query_clean = clean_text(query_abstract)
        query_vec = self.vectorizer.transform([query_clean])
        similarities = linear_kernel(query_vec, self.doc_matrix).flatten()

        candidate_pool = min(max(candidate_pool, top_k), len(similarities))
        top_doc_idx = similarities.argsort()[::-1][:candidate_pool]

        score_by_journal = {}
        count_by_journal = {}
        sample_title_by_journal = {}
        sample_year_by_journal = {}

        for idx in top_doc_idx:
            journal = self.journals.iloc[idx]
            score = float(similarities[idx])
            score_by_journal[journal] = score_by_journal.get(journal, 0.0) + score
            count_by_journal[journal] = count_by_journal.get(journal, 0) + 1
            sample_title_by_journal.setdefault(journal, self.titles.iloc[idx])
            sample_year_by_journal.setdefault(journal, self.years.iloc[idx])

        ranked = sorted(score_by_journal.items(), key=lambda item: item[1], reverse=True)[:top_k]
        return [
            {
                "rank": rank,
                "journal_name": journal,
                "score_sum": round(score_sum, 6),
                "matched_docs": count_by_journal[journal],
                "example_title": sample_title_by_journal[journal],
                "example_year": sample_year_by_journal[journal],
            }
            for rank, (journal, score_sum) in enumerate(ranked, start=1)
        ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommend the top-k journals for a query abstract.")
    parser.add_argument("--input", default="outputs/base_articles_clean.csv", help="Clean dataset CSV.")
    parser.add_argument("--query", required=True, help="Abstract text to query.")
    parser.add_argument("--top-k", type=int, default=5, help="Number of journals to return.")
    parser.add_argument("--candidate-pool", type=int, default=300, help="Top similar documents to aggregate.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    model = JournalRecommender.from_dataframe(df)
    recommendations = model.recommend(args.query, top_k=args.top_k, candidate_pool=args.candidate_pool)

    print("Top journal recommendations:")
    for row in recommendations:
        print(
            f"{row['rank']}. {row['journal_name']} | score_sum={row['score_sum']} "
            f"| matched_docs={row['matched_docs']} | example_year={row['example_year']}"
        )


if __name__ == "__main__":
    main()
