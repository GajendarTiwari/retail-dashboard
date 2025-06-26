import pandas as pd
import os

# Paths
clv_path = "analysis/clv/clv_summary.csv"
segments_path = "analysis/segments/hshd_segments.csv"
output_path = "analysis/clv/clv_with_segments.csv"

# Load data
df_clv = pd.read_csv(clv_path)
df_segments = pd.read_csv(segments_path)

# Merge on HSHD_NUM
df_merged = pd.merge(df_clv, df_segments, on="HSHD_NUM", how="left")

# Save the combined result
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_merged.to_csv(output_path, index=False)

print("✅ Merged CLV with Segments saved to:", output_path)
print(df_merged.head())
