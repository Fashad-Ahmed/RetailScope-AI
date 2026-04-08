from pathlib import Path
import os
import numpy as np

import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Load environment variables
try:
    from dotenv import load_dotenv
    _root = Path(__file__).resolve().parent.parent.parent
    load_dotenv(_root / ".env")
except ImportError:
    pass

DB_URL = os.getenv("DB_URL")


def main():
    engine = create_engine(DB_URL)

    query = """
        SELECT customer_id, recency, frequency, monetary
        FROM mart_customer_rfm
    """

    df = pd.read_sql(query, engine)

    print("Loaded data shape:", df.shape)

    df["monetary"] = np.log1p(df["monetary"])
    df["frequency"] = np.log1p(df["frequency"])

    features = df[["recency", "frequency", "monetary"]]

    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    k_values = range(2, 11)

    inertia = []
    silhouette = []

    print("\nEvaluating K values...\n")

    for k in k_values:
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = model.fit_predict(X)

        inertia.append(model.inertia_)
        score = silhouette_score(X, labels)
        silhouette.append(score)

        print(f"K={k}, inertia={model.inertia_:.2f}, silhouette={score:.3f}")


    plt.figure()
    plt.plot(k_values, inertia, marker="o")
    plt.title("Elbow Method")
    plt.xlabel("K")
    plt.ylabel("Inertia")
    plt.show()

    plt.figure()
    plt.plot(k_values, silhouette, marker="o")
    plt.title("Silhouette Score")
    plt.xlabel("K")
    plt.ylabel("Score")
    plt.show()

    best_k = k_values[silhouette.index(max(silhouette))]
    print("\nBest K (auto):", best_k)

    best_k = 4
    print("Final K used:", best_k)

    final_model = KMeans(
        n_clusters=best_k,
        random_state=42,
        n_init=10
    )

    df["segment"] = final_model.fit_predict(X)


    print("\nSegment Distribution:\n")
    print(df["segment"].value_counts())

    profile = df.groupby("segment").agg({
        "recency": "mean",
        "frequency": "mean",
        "monetary": "mean",
        "customer_id": "count"
    }).rename(columns={"customer_id": "num_customers"})

    print("\nCluster Profile:\n", profile)

    profile_scaled = (profile - profile.min()) / (profile.max() - profile.min())
    print("\nNormalized Profile:\n", profile_scaled)

    df[["customer_id", "segment"]].to_sql(
        "mart_customer_segments",
        engine,
        if_exists="replace",
        index=False
    )

    profile.reset_index().to_sql(
        "mart_customer_segment_profile",
        engine,
        if_exists="replace",
        index=False
    )

    print("\nSegments + profiles stored successfully")


if __name__ == "__main__":
    main()