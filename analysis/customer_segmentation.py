import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load summary data
summary_path = "analysis/analysis/hshd_summary_output.csv"  # adjust path as needed
df = pd.read_csv(summary_path)

# Standardize the features
features = ["TOTAL_SPEND", "TOTAL_UNITS", "TRANSACTIONS"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[features])

# Elbow Method (Optional: use this to determine best cluster count)
# distortions = []
# for k in range(1, 10):
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(X_scaled)
#     distortions.append(kmeans.inertia_)
# plt.plot(range(1, 10), distortions, marker='o')
# plt.xlabel('Number of clusters')
# plt.ylabel('Distortion')
# plt.title('Elbow Method')
# plt.show()

# Fit KMeans with optimal number of clusters (e.g., 4)
kmeans = KMeans(n_clusters=4, random_state=42)
df["SEGMENT"] = kmeans.fit_predict(X_scaled)

# Save the results
output_dir = "analysis/segments"
os.makedirs(output_dir, exist_ok=True)
df.to_csv(os.path.join(output_dir, "hshd_segments.csv"), index=False)

print("✅ Segmentation completed and saved to analysis/segments/hshd_segments.csv")
print(df.groupby("SEGMENT").agg({
    "TOTAL_SPEND": "mean",
    "TOTAL_UNITS": "mean",
    "TRANSACTIONS": "mean",
    "HSHD_NUM": "count"
}).rename(columns={"HSHD_NUM": "NUM_CUSTOMERS"}))
