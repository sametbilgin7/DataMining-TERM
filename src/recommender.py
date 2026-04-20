import argparse
from dataclasses import dataclass

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


@dataclass
class JournalRecommender:
    vectorizer: TfidfVectorizer
    doc_matrix: any
    journals: pd.Series

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        text_col: str = "abstract_clean",
        journal_col: str = "journal_name",
        max_features: int = 50000,
        ngram_range: tuple = (1, 2),
        min_df: int = 3,
        max_df: float = 0.9,
    ) -> "JournalRecommender":
        if text_col not in df.columns or journal_col not in df.columns:
            raise ValueError(f"DataFrame must contain '{text_col}' and '{journal_col}' columns.")

        work = df[[text_col, journal_col]].dropna().copy()
        work[text_col] = work[text_col].astype(str).str.strip()
        work[journal_col] = work[journal_col].astype(str).str.strip()
        work = work[(work[text_col] != "") & (work[journal_col] != "")]

        vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            norm="l2",
        )
        doc_matrix = vectorizer.fit_transform(work[text_col])
        return cls(vectorizer=vectorizer, doc_matrix=doc_matrix, journals=work[journal_col].reset_index(drop=True))

    def recommend(self, query_abstract: str, top_k: int = 5, candidate_pool: int = 300):
        if not isinstance(query_abstract, str) or not query_abstract.strip():
            raise ValueError("query_abstract must be a non-empty string.")

        query_vec = self.vectorizer.transform([query_abstract])
        similarities = linear_kernel(query_vec, self.doc_matrix).flatten()

        if candidate_pool <= 0:
            candidate_pool = min(300, len(similarities))
        candidate_pool = min(candidate_pool, len(similarities))

        top_doc_idx = similarities.argsort()[::-1][:candidate_pool]
        candidate_scores = similarities[top_doc_idx]

        score_by_journal = {}
        count_by_journal = {}
        for idx, score in zip(top_doc_idx, candidate_scores):
            journal = self.journals.iloc[idx]
            score_by_journal[journal] = score_by_journal.get(journal, 0.0) + float(score)
            count_by_journal[journal] = count_by_journal.get(journal, 0) + 1

        ranked = sorted(score_by_journal.items(), key=lambda x: x[1], reverse=True)[:top_k]
        result = []
        for rank, (journal, score_sum) in enumerate(ranked, start=1):
            result.append(
                {
                    "rank": rank,
                    "journal_name": journal,
                    "score_sum": round(score_sum, 6),
                    "matched_docs": count_by_journal[journal],
                }
            )
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommend top-k journals from an abstract.")
    parser.add_argument("--input", default="outputs/base_articles_clean.csv", help="Path to cleaned dataset CSV.")
    parser.add_argument("--query", required=True, help="Abstract text query for journal recommendation.")
    parser.add_argument("--top-k", type=int, default=5, help="Number of journals to return.")
    parser.add_argument(
        "--candidate-pool",
        type=int,
        default=300,
        help="Top similar documents to aggregate journal scores from.",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    model = JournalRecommender.from_dataframe(df)
    recommendations = model.recommend(args.query, top_k=args.top_k, candidate_pool=args.candidate_pool)

    print("Top journal recommendations:")
    for row in recommendations:
        print(
            f"{row['rank']}. {row['journal_name']} | score_sum={row['score_sum']} | matched_docs={row['matched_docs']}"
        )


if __name__ == "__main__":
    main()
