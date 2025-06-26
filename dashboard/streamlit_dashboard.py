import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.set_page_config(layout="wide")
st.title("🛒 Retail Insights Dashboard")

# === Load Data ===
@st.cache_data
def load_data():
    summary_path = "analysis/analysis/analysis/hshd_summary_output.csv"
    clv_path = "analysis/analysis/clv/clv_summary.csv"
    segments_path = "analysis/analysis/segments/hshd_segments.csv"
    recommendations_path = "analysis/analysis/recommendations/top_products_per_segment.csv"
    products_path = "data/400_products.csv"
    churn_preds_path = "analysis/analysis/analysis/churn/churn_predictions.csv"
    frequent_itemsets_path = "analysis/analysis/analysis/basket/frequent_itemsets.csv"
    association_rules_path = "analysis/analysis/analysis/basket/association_rules.csv"

    return {
        "summary": pd.read_csv(summary_path),
        "clv": pd.read_csv(clv_path),
        "segments": pd.read_csv(segments_path),
        "recommendations": pd.read_csv(recommendations_path),
        "products": pd.read_csv(products_path),
        "churn_preds": pd.read_csv(churn_preds_path),
        "frequent_itemsets": pd.read_csv(frequent_itemsets_path),
        "association_rules": pd.read_csv(association_rules_path)
    }

data = load_data()

# Clean columns
data["products"].columns = data["products"].columns.str.strip()

# === LAYOUT ===
col1, col2 = st.columns(2)

# 🔍 CLV DISTRIBUTION BY SEGMENT
with col1:
    st.subheader("💰 CLV Distribution by Segment")
    merged = data["clv"].merge(data["segments"], on="HSHD_NUM", how="left")
    fig = px.box(merged, x="SEGMENT", y="CLV", color="SEGMENT", color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("🎯 Insight: Compare CLV distributions across customer segments to identify high-value groups.")

# 🎯 TOP PRODUCTS PER SEGMENT
with col2:
    st.subheader("🏆 Top Products by Segment")
    merged_reco = data["recommendations"].merge(data["products"], on="PRODUCT_NUM", how="left")
    top_n = st.slider("Select top N products", 5, 20, 10)
    top_data = merged_reco.groupby("SEGMENT").apply(lambda df: df.nlargest(top_n, "TOTAL_SPEND")).reset_index(drop=True)
    fig = px.bar(top_data, x="PRODUCT_NUM", y="TOTAL_SPEND", color="SEGMENT", barmode="group",
                 title="Segment-wise Top Spending Products", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("🧺 Insight: Know which products drive revenue in each segment.")

# 📉 CHURN PREDICTION DISTRIBUTION
st.subheader("⚠️ Churn Prediction Overview")
if "CHURNED" in data["churn_preds"].columns:
    churned_count = data["churn_preds"]["CHURNED"].value_counts().reset_index()
    churned_count.columns = ["CHURNED", "count"]
    fig = px.pie(churned_count, names="CHURNED", values="count", title="Customer Churn Distribution",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("📌 Insight: Understand how many customers are at risk of leaving.")

# 📊 FREQUENT ITEMSETS
st.subheader("🧾 Frequent Items Bought Together")
if not data["frequent_itemsets"].empty:
    data["frequent_itemsets"]["itemsets"] = data["frequent_itemsets"]["itemsets"].astype(str)
    fig = px.bar(data["frequent_itemsets"].nlargest(10, "support"),
                 x="itemsets", y="support", color="support", color_continuous_scale="Tealgrn",
                 title="Top 10 Frequent Itemsets")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("📦 Insight: Common combinations of items purchased together.")

# 🔗 ASSOCIATION RULES
st.subheader("🔗 Association Rules (Cross-sell Opportunities)")
if not data["association_rules"].empty:
    rules = data["association_rules"].copy()
    rules["antecedents"] = rules["antecedents"].astype(str)
    rules["consequents"] = rules["consequents"].astype(str)
    fig = px.scatter(rules, x="support", y="confidence", color="lift", hover_data=["antecedents", "consequents"],
                     title="Association Rules: Support vs Confidence",
                     color_continuous_scale="Plasma")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("🤝 Insight: Strong lift & confidence indicate great cross-selling opportunities.")
else:
    st.warning("⚠️ No association rules found. Please check if basket_analysis generated rules.")

# 📋 RAW SUMMARY TABLE
st.subheader("📋 Household Summary Snapshot")
st.dataframe(data["summary"].head(10), use_container_width=True)
st.caption("📑 Snapshot of household-level retail transactions.")

st.markdown("---")
st.markdown("✅ Dashboard Loaded | Powered by Streamlit | 📊")

