import os
import pandas as pd
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Transaction

def summarize_hshd_data():
    db: Session = SessionLocal()
    transactions = db.query(Transaction).all()

    data = []
    for t in transactions:
        try:
            data.append({
                "HSHD_NUM": t.hshd_num,
                "SPEND": t.spend,
                "UNITS": t.units,
                "YEAR": t.year,
                "WEEK": t.week_num
            })
        except Exception as e:
            print(f"⚠️ Skipping transaction due to error: {e}")

    df = pd.DataFrame(data)

    if df.empty:
        print("❌ No transaction data to summarize.")
        return pd.DataFrame()

    summary = df.groupby("HSHD_NUM").agg(
        TOTAL_SPEND=pd.NamedAgg(column="SPEND", aggfunc="sum"),
        TOTAL_UNITS=pd.NamedAgg(column="UNITS", aggfunc="sum"),
        TRANSACTIONS=pd.NamedAgg(column="WEEK", aggfunc="count")
    ).reset_index()

    print("✅ Household-level summary:")
    print(summary.head())
    return summary

if __name__ == "__main__":
    result = summarize_hshd_data()

    # ✅ Updated to match your real directory
    output_dir = os.path.join("analysis", "analysis")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "hshd_summary_output.csv")
    result.to_csv(output_path, index=False)
    print(f"📁 Summary saved to {output_path}")
