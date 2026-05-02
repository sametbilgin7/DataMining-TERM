import argparse

import pandas as pd
from sklearn.model_selection import train_test_split

from recommender import JournalRecommender


def hit_at_k(
    df: pd.DataFrame,
    sample_size: int = 500,
    test_size: float = 0.2,
    random_state: int = 42,
    k: int = 5,
) -> float:
    label_counts = df["journal_name"].value_counts()
    can_stratify = bool((label_counts >= 2).all())
    stratify = df["journal_name"] if can_stratify else None

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )
    model = JournalRecommender.from_dataframe(train_df)

    sample_size = min(sample_size, len(test_df))
    test_sample = test_df.sample(n=sample_size, random_state=random_state)

    hits = 0
    for _, row in test_sample.iterrows():
        pred = model.recommend(row["abstract_text"], top_k=k)
        pred_journals = {item["journal_name"] for item in pred}
        if row["journal_name"] in pred_journals:
            hits += 1

    return hits / sample_size if sample_size else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the journal finder with Hit@K.")
    parser.add_argument("--input", default="outputs/base_articles_clean.csv", help="Clean dataset CSV.")
    parser.add_argument("--sample-size", type=int, default=300, help="Number of test samples.")
    parser.add_argument("--k", type=int, default=5, help="Recommendation list length.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    score = hit_at_k(df, sample_size=args.sample_size, k=args.k)
    print(f"Hit@{args.k} (sample={args.sample_size}): {score:.4f}")


if __name__ == "__main__":
    main()
