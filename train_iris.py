import pandas as pd
import joblib
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Load data
df = pd.read_csv(
    "https://raw.githubusercontent.com/erkansirin78/datasets/master/iris.csv"
)

X = df.iloc[:, :-1].values
y = df.iloc[:, -1]

# Label encoder
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# Split test train
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.33, random_state=42
)

# Train model
print("Training Iris model...")
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X_train, y_train)

# Test model
y_pred = classifier.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Save model and encoder
os.makedirs("saved_models", exist_ok=True)
joblib.dump(classifier, "saved_models/iris_model.pkl")
joblib.dump(encoder, "saved_models/label_encoder.pkl")
print("Iris model and label encoder saved to saved_models/")
