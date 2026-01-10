import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Load data
df = pd.read_csv(
    "https://raw.githubusercontent.com/erkansirin78/datasets/master/Advertising.csv"
)

# Feature matrix and Output variable
X = df.iloc[:, 1:-1].values
y = df.iloc[:, -1]

# Split test train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

# Train model
print("Training Advertising model...")
estimator = RandomForestRegressor(n_estimators=200)
estimator.fit(X_train, y_train)

# Test model
y_pred = estimator.predict(X_test)
print(f"R2 Score: {r2_score(y_true=y_test, y_pred=y_pred)}")

# Save as pickle
os.makedirs("saved_models", exist_ok=True)
model_path = "saved_models/advertising_model.pkl"
joblib.dump(estimator, model_path)
print(f"Model saved to {model_path}")
