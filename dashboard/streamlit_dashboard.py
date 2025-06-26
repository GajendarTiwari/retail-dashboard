import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set Streamlit page config
st.set_page_config(page_title="Retail Insights Dashboard", layout="wide")

# File paths
summary_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\analysis\analysis\analysis\hshd_summary_output.csv"
clv_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\analysis\analysis\clv\clv_summary.csv"
segments_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\analysis\analysis\segments\hshd_segments.csv"
reco_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\analysis\analysis\recommendations\top_products_per_segment.csv"
products_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\data\400_products.csv"
frequent_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\analysis\analysis\analysis\basket\frequent_itemsets.csv"
assoc_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\analysis\analysis\analysis\basket\association_rules.csv"
churn_preds_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\analysis\analysis\analysis\churn\churn_predictions.csv"

# Load data safely with caching
@st.cache_data

def load_data():
    return {
        "summary": pd.read_csv(summary_path),
        "clv": pd.read_csv(clv_path),
        "segments": pd.read_csv(segments_path),
        "recommendations": pd.read_csv(reco_path),
        "products": pd.read_csv(products_path).rename(columns=lambda x: x.strip()),
        "frequent": pd.read_csv(frequent_path),
        "association": pd.read_csv(assoc_path),
        "churn_preds": pd.read_csv(churn_preds_path),
    }

# Load data
data = load_data()

st.title("🛒 Retail Insights & Customer Engagement Dashboard")
st.markdown("---")

# 📊 Section 1: Household Spend Summary
st.header("📈 Household Spend Summary")
fig1 = px.bar(
    data["summary"].sort_values("TOTAL_SPEND", ascending=False).head(15),
    x="HSHD_NUM", y="TOTAL_SPEND", color="TOTAL_UNITS",
    title="Top 15 Households by Total Spend",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig1, use_container_width=True)
st.caption("🔍 This bar chart shows which households are the top spenders and their respective purchase volumes.")

# 💳 Section 2: CLV & Segmentation
st.header("💰 Customer Lifetime Value (CLV) by Segment")
clv_seg = data["clv"].merge(data["segments"], on="HSHD_NUM", how="left")
fig2 = px.box(
    clv_seg, x="SEGMENT", y="CLV", color="SEGMENT",
    title="CLV Distribution per Segment", color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig2, use_container_width=True)
st.caption("💡 Use this boxplot to identify which segments bring in long-term value and can be targeted for loyalty programs.")

# 🛍️ Section 3: Top Product Recommendations
st.header("🎯 Top Product Recommendations per Segment")
top_df = data["recommendations"].merge(data["products"], on="PRODUCT_NUM", how="left")
fig3 = px.bar(
    top_df.sort_values("TOTAL_SPEND", ascending=False).head(20),
    x="COMMODITY", y="TOTAL_SPEND", color="SEGMENT", barmode="group",
    title="Top Products by Segment",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig3, use_container_width=True)
st.caption("🧠 Understand which specific commodities are most purchased by each customer segment.")

# 🧺 Section 4: Frequently Bought Together
st.header("🧺 Frequently Bought Together (Frequent Itemsets)")
freq = data["frequent"].copy()
freq["itemsets"] = freq["itemsets"].astype(str)
fig4 = px.bar(
    freq.sort_values("support", ascending=False).head(10),
    x="itemsets", y="support",
    color_discrete_sequence=["#F08080"],
    title="Top 10 Itemsets Frequently Bought Together"
)
st.plotly_chart(fig4, use_container_width=True)
st.caption("📦 Use these insights for product bundling and cross-sell promotions.")

# 🔄 Section 5: Churn Prediction Overview
st.header("📉 Churn Prediction Overview")
fig5 = px.histogram(
    data["churn_preds"], x="PREDICTED_CHURN", color="PREDICTED_CHURN",
    color_discrete_sequence=["#8B0000", "#2E8B57"],
    title="Predicted Churn Distribution"
)
st.plotly_chart(fig5, use_container_width=True)
st.caption("🚨 This shows how many households are at risk of churn and may require re-engagement.")

# 📄 Footer
st.markdown("---")
st.markdown("✅ **Dashboard Built with Streamlit | Powered by Machine Learning, Apriori & Visual Insights**")
st.markdown("📍 Data Source: 84.51° / Kroger Sample Retail Dataset")
