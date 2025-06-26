import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

# ✅ Load household summary (used to create churn features)
summary_path = r"C:\Users\Admin\OneDrive\Desktop\Data Analysis project\retail_project\analysis\analysis\analysis\hshd_summary_output.csv"


df = pd.read_csv(summary_path)

# 🧪 Simulate churn flag (you can adjust logic)
df["CHURNED"] = np.where(df["TRANSACTIONS"] < 100, 1, 0)

# 🔧 Select features
features = ["TOTAL_SPEND", "TOTAL_UNITS", "TRANSACTIONS"]
target = "CHURNED"
X = df[features]
y = df[target]

# 📊 Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 🤖 Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔮 Predictions
df["PREDICTED_CHURN"] = model.predict(X)
y_pred = model.predict(X_test)

# 📈 Feature importance
importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

# 📁 Output files
output_dir = r"analysis/analysis/churn"
os.makedirs(output_dir, exist_ok=True)

df.to_csv(os.path.join(output_dir, "churn_features.csv"), index=False)
df[["HSHD_NUM", "CHURNED", "PREDICTED_CHURN"]].to_csv(os.path.join(output_dir, "churn_predictions.csv"), index=False)
importance_df.to_csv(os.path.join(output_dir, "feature_importance.csv"), index=False)

# 🧾 Report
print("🔍 Classification Report:")
print(classification_report(y_test, y_pred))
print("✅ churn_features.csv saved")
print("✅ churn_predictions.csv saved")
print("✅ feature_importance.csv saved")
