import os
import pandas as pd
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Transaction

def calculate_clv():
    db: Session = SessionLocal()
    transactions = db.query(Transaction).all()

    data = []
    for t in transactions:
        try:
            data.append({
                "HSHD_NUM": t.hshd_num,
                "SPEND": t.spend,
                "YEAR": t.year,
                "WEEK": t.week_num
            })
        except Exception as e:
            print(f"⚠️ Skipping due to error: {e}")

    df = pd.DataFrame(data)

    if df.empty:
        print("❌ No data available.")
        return pd.DataFrame()

    grouped = df.groupby("HSHD_NUM").agg(
        total_spend=pd.NamedAgg(column="SPEND", aggfunc="sum"),
        transaction_count=pd.NamedAgg(column="WEEK", aggfunc="count")
    ).reset_index()

    grouped["avg_spend_per_txn"] = grouped["total_spend"] / grouped["transaction_count"]
    grouped["avg_txns_per_month"] = grouped["transaction_count"] / 12  # ~1 year data
    grouped["customer_lifetime_months"] = 12  # assuming 1-year lifetime
    grouped["CLV"] = (
            grouped["avg_spend_per_txn"] *
            grouped["avg_txns_per_month"] *
            grouped["customer_lifetime_months"]
    ).round(2)

    print("✅ Calculated CLV:")
    print(grouped[["HSHD_NUM", "CLV"]].head())

    # Save result
    output_dir = os.path.join("analysis", "clv")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "clv_summary.csv")
    grouped.to_csv(output_path, index=False)
    print(f"📁 CLV summary saved to: {output_path}")

    return grouped

if __name__ == "__main__":
    calculate_clv()
