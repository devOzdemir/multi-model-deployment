import os
import requests
import zipfile
import shutil


def setup_datasets():
    """
    Downloads and prepares the sentiment datasets as per the requirements.
    Following the structure: data/sentiment_labeled_sentences/
    """
    # 1. Define paths
    base_data_dir = "data"
    zip_path = os.path.join(base_data_dir, "sentiment_labeled_sentences.zip")
    extract_path = os.path.join(base_data_dir, "temp_extract")
    final_dir = os.path.join(base_data_dir, "sentiment_labeled_sentences")

    # Target files to verify
    target_files = [
        "yelp_labelled.txt",
        "amazon_cells_labelled.txt",
        "imdb_labelled.txt",
    ]

    # URL from the assignment screenshot
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00331/sentiment%20labelled%20sentences.zip"

    # 2. Create data directory
    if not os.path.exists(base_data_dir):
        os.makedirs(base_data_dir)
        print(f"Created directory: {base_data_dir}")

    # 3. Download the zip file
    if not os.path.exists(zip_path):
        print(f"Downloading dataset from {url}...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(zip_path, "wb") as f:
                f.write(response.content)
            print("Download complete.")
        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return
    else:
        print("Zip file already exists, skipping download.")

    # 4. Unzip the file
    print("Extracting files...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)

    # 5. Move files to the correct location (cleaning up nested folder)
    # The zip usually contains a folder named 'sentiment labelled sentences'
    nested_folder = os.path.join(extract_path, "sentiment labelled sentences")

    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    for file_name in target_files:
        src = os.path.join(nested_folder, file_name)
        dst = os.path.join(final_dir, file_name)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Moved: {file_name}")

    # 6. Cleanup
    shutil.rmtree(extract_path)
    # Optional: remove zip file after extraction
    # os.remove(zip_path)

    print(f"\nSuccess! Datasets are ready in: {final_dir}")


if __name__ == "__main__":
    setup_datasets()
