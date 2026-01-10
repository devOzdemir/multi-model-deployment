import pandas as pd
import os
import pickle
import numpy as np
import joblib
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

# Define internal project paths for portability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

os.makedirs(MODEL_DIR, exist_ok=True)

# Data files inside the project directory
filepath_dict = {
    "yelp": os.path.join(DATA_DIR, "yelp_labelled.txt"),
    "amazon": os.path.join(DATA_DIR, "amazon_cells_labelled.txt"),
    "imdb": os.path.join(DATA_DIR, "imdb_labelled.txt"),
}


def load_local_data():
    """Loads datasets from the local data/ folder."""
    df_list = []
    for source, filepath in filepath_dict.items():
        if os.path.exists(filepath):
            # Files are tab-separated with no header as seen in original code
            df = pd.read_csv(filepath, names=["sentence", "label"], sep="\t")
            df["source"] = source
            df_list.append(df)
        else:
            print(
                f"Error: {filepath} not found! Please place datasets in data/ folder."
            )

    if not df_list:
        raise FileNotFoundError("No dataset files found in the data/ directory.")
    return pd.concat(df_list)


# Main Execution Flow
df = load_local_data()
df_yelp = df[df["source"] == "yelp"]
sentences = df_yelp["sentence"].values
y = df_yelp["label"].values

# Split data (Fixed variables names to avoid errors)
sentences_train, sentences_test, y_train, y_test = train_test_split(
    sentences, y, test_size=0.25, random_state=1000
)

# Text Preprocessing
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(sentences_train)

X_train = tokenizer.texts_to_sequences(sentences_train)
X_test = tokenizer.texts_to_sequences(sentences_test)

vocab_size = len(tokenizer.word_index) + 1
maxlen = 100

X_train = pad_sequences(X_train, padding="post", maxlen=maxlen)
X_test = pad_sequences(X_test, padding="post", maxlen=maxlen)

# Model Definition (CNN/Dense Architecture)
model = Sequential(
    [
        layers.Embedding(input_dim=vocab_size, output_dim=50),
        layers.GlobalMaxPool1D(),
        layers.Dense(10, activation="relu"),
        layers.Dense(1, activation="sigmoid"),
    ]
)

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Training (No MLflow tracking as per instructions)
print("Starting DL model training...")
model.fit(
    X_train,
    y_train,
    epochs=20,
    verbose=1,
    validation_data=(X_test, y_test),
    batch_size=10,
)

with open(os.path.join(MODEL_DIR, "tokenizer.pkl"), "wb") as f:
    pickle.dump(tokenizer, f)

model_path = os.path.join(MODEL_DIR, "tensorflow_model.pkl")
joblib.dump(model, model_path)

print(f"TensorFlow model saved as pickle to {model_path}")
