import pandas as pd
import os
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Transaction

# Load segmentation
segments_df = pd.read_csv("analysis/segments/hshd_segments.csv")

# Load transactions
db: Session = SessionLocal()
transactions = db.query(Transaction).all()

data = []
for t in transactions:
    data.append({
        "HSHD_NUM": t.hshd_num,
        "PRODUCT_NUM": t.product_num,
        "SPEND": t.spend,
        "UNITS": t.units
    })

df_tx = pd.DataFrame(data)

# Merge with segment info
df_combined = pd.merge(df_tx, segments_df[["HSHD_NUM", "SEGMENT"]], on="HSHD_NUM", how="left")

# Top products per segment
recommendations = (
    df_combined
    .groupby(["SEGMENT", "PRODUCT_NUM"])
    .agg(TOTAL_SPEND=("SPEND", "sum"), PURCHASES=("UNITS", "sum"))
    .reset_index()
)

# Get top 5 products per segment
top_products = (
    recommendations
    .sort_values(["SEGMENT", "PURCHASES"], ascending=[True, False])
    .groupby("SEGMENT")
    .head(5)
)

# Save recommendations
os.makedirs("analysis/recommendations", exist_ok=True)
top_products.to_csv("analysis/recommendations/top_products_per_segment.csv", index=False)

print("✅ Saved top product recommendations per segment.")
print(top_products.head(10))
