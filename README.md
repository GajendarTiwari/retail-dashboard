# 🛒 Retail Dashboard (84.51°/Kroger Data Analysis)

Welcome to the **Retail Intelligence Dashboard** — an end-to-end analytics project built using real-world retail data from 84.51°/Kroger. This project uses cloud-compatible tools (e.g., Streamlit, pandas, scikit-learn) and visual dashboards to provide actionable insights into customer behavior, segmentation, churn risk, and product strategy.

🔗 **Live Dashboard**: [Click here to explore](https://retail-dashboard-2qjzzbgwp869rolzl9ndod.streamlit.app)

---

## 📊 Key Features

### ✅ Customer Lifetime Value (CLV)
- Segment-wise CLV boxplots
- Understand long-term value by demographics

### ✅ Top Products per Segment
- Product-wise spending distribution
- Ideal for targeted marketing

### ✅ Churn Prediction
- ML-based churn classification
- Visual churn distribution & feature importance

### ✅ Basket Insights
- Apriori-based frequent itemsets
- Association rules for cross-selling strategies

### ✅ Household Summary Viewer
- HSHD_NUM-level breakdown of spend, units, and transactions

---

## 🧠 ML Models Used

| Model               | Usage                       |
|--------------------|-----------------------------|
| **Random Forest**  | Churn classification        |
| **Linear Regression** | CLV estimation             |
| **Apriori**        | Market basket analysis      |

---

## 🧱 Tech Stack

- **Frontend**: Streamlit
- **Backend/Logic**: Python, pandas, scikit-learn, mlxtend
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Database (optional)**: MySQL (for raw ingestion)
- **Hosting**: [Streamlit Cloud](https://streamlit.io/cloud)

---

## 📂 Folder Structure

```bash
├── dashboard/
│   └── streamlit_dashboard.py
├── analysis/
│   ├── churn/
│   ├── clv/
│   ├── basket/
│   └── segments/
├── data/
│   └── 400_products.csv
├── requirements.txt
