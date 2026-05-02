import argparse

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score


def top_terms_per_cluster(model: KMeans, vectorizer: TfidfVectorizer, top_n: int = 10) -> dict[int, list[str]]:
    terms = vectorizer.get_feature_names_out()
    centroids = model.cluster_centers_
    result = {}
    for cluster_id, center in enumerate(centroids):
        top_idx = center.argsort()[::-1][:top_n]
        result[cluster_id] = [terms[i] for i in top_idx]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Cluster CS journal article topics.")
    parser.add_argument("--input", default="outputs/base_articles_clean.csv", help="Clean dataset CSV.")
    parser.add_argument("--k", type=int, default=8, help="Number of clusters.")
    parser.add_argument("--max-features", type=int, default=30000, help="TF-IDF vocabulary cap.")
    parser.add_argument("--output", default="outputs/topic_clusters.csv", help="Cluster output CSV.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    text = df["model_text"].fillna("").astype(str)

    vectorizer = TfidfVectorizer(
        max_features=args.max_features,
        ngram_range=(1, 2),
        min_df=3,
        max_df=0.9,
        sublinear_tf=True,
    )
    matrix = vectorizer.fit_transform(text)

    kmeans = KMeans(n_clusters=args.k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(matrix)

    cluster_terms = top_terms_per_cluster(kmeans, vectorizer, top_n=10)
    silhouette = silhouette_score(matrix, labels)

    out = df[["record_id", "journal_name", "pub_year", "subject_terms"]].copy()
    out["cluster_id"] = labels
    out.to_csv(args.output, index=False)

    print(f"Saved cluster assignments to: {args.output}")
    print(f"Silhouette score: {silhouette:.4f}")
    print("Top terms per cluster:")
    for cluster_id in sorted(cluster_terms):
        print(f"Cluster {cluster_id}: {', '.join(cluster_terms[cluster_id])}")


if __name__ == "__main__":
    main()
