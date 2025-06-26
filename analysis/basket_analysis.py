import os
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Transaction

def load_transactions():
    db: Session = SessionLocal()
    transactions = db.query(Transaction).all()

    data = []
    for t in transactions:
        try:
            data.append({
                "HSHD_NUM": t.hshd_num,
                "BASKET_NUM": t.basket_num,
                "PRODUCT_NUM": str(t.product_num)
            })
        except Exception as e:
            print(f"⚠️ Skipping transaction due to error: {e}")
    return pd.DataFrame(data)

def filter_top_products(df, top_n=500):
    top_products = df["PRODUCT_NUM"].value_counts().nlargest(top_n).index
    return df[df["PRODUCT_NUM"].isin(top_products)]

def filter_sparse_baskets(df, max_products_per_basket=20):
    basket_sizes = df.groupby("BASKET_NUM")["PRODUCT_NUM"].nunique()
    valid_baskets = basket_sizes[basket_sizes <= max_products_per_basket].index
    return df[df["BASKET_NUM"].isin(valid_baskets)]

def generate_basket_matrix(df):
    basket_df = df.groupby(["BASKET_NUM", "PRODUCT_NUM"]).size().unstack(fill_value=0)
    basket_df = basket_df.astype(bool)  # Proper boolean conversion
    return basket_df

def perform_apriori(basket_df, support_threshold=0.005, lift_threshold=0.5):
    frequent_itemsets = apriori(basket_df, min_support=support_threshold, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=lift_threshold)
    return frequent_itemsets, rules

if __name__ == "__main__":
    print("🔄 Loading transaction data...")
    df = load_transactions()

    if df.empty:
        print("❌ No transactions to process.")
        exit()

    print(f"✅ Loaded {len(df)} transactions")

    df = filter_top_products(df, top_n=500)
    print(f"✅ Retained top {df['PRODUCT_NUM'].nunique()} products")

    df = filter_sparse_baskets(df, max_products_per_basket=20)
    print(f"✅ Retained {df['BASKET_NUM'].nunique()} baskets with ≤ 20 products")

    print("📊 Creating basket matrix...")
    basket_matrix = generate_basket_matrix(df)

    print("🧠 Running Apriori algorithm...")
    frequent_itemsets, rules = perform_apriori(basket_matrix)

    output_dir = os.path.join("analysis", "analysis", "basket")
    os.makedirs(output_dir, exist_ok=True)

    fi_path = os.path.join(output_dir, "frequent_itemsets.csv")
    rules_path = os.path.join(output_dir, "association_rules.csv")

    frequent_itemsets.to_csv(fi_path, index=False)
    rules.to_csv(rules_path, index=False)

    print(f"✅ Frequent itemsets saved to: {fi_path}")
    print(f"✅ Association rules saved to: {rules_path}")
    print(f"🔍 Rules generated: {len(rules)}")
