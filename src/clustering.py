import argparse

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score


def top_terms_per_cluster(model: KMeans, vectorizer: TfidfVectorizer, top_n: int = 10):
    terms = vectorizer.get_feature_names_out()
    centroids = model.cluster_centers_
    results = {}
    for cluster_id, center in enumerate(centroids):
        top_idx = center.argsort()[::-1][:top_n]
        results[cluster_id] = [terms[i] for i in top_idx]
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Topic clustering over cleaned abstracts.")
    parser.add_argument("--input", default="outputs/base_articles_clean.csv")
    parser.add_argument("--k", type=int, default=8)
    parser.add_argument("--max-features", type=int, default=30000)
    parser.add_argument("--output", default="outputs/topic_clusters.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    text = df["abstract_clean"].fillna("").astype(str)

    vectorizer = TfidfVectorizer(max_features=args.max_features, ngram_range=(1, 2), min_df=3, max_df=0.9)
    X = vectorizer.fit_transform(text)

    kmeans = KMeans(n_clusters=args.k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    df_out = df[["record_id", "journal_name", "pub_year"]].copy()
    df_out["cluster_id"] = labels
    df_out.to_csv(args.output, index=False)

    sil = silhouette_score(X, labels)
    terms = top_terms_per_cluster(kmeans, vectorizer, top_n=10)

    print(f"Saved cluster assignments to: {args.output}")
    print(f"Silhouette score: {sil:.4f}")
    print("Top terms per cluster:")
    for cid in sorted(terms):
        print(f"Cluster {cid}: {', '.join(terms[cid])}")


if __name__ == "__main__":
    main()
