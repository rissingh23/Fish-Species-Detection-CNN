import os
import kagglehub
import zipfile
import shutil

def download_fish_dataset(dest_dir="data"):
    os.makedirs(dest_dir, exist_ok=True)

    # 1) download — might return a .zip path or a directory
    path = kagglehub.dataset_download(
        "crowww/a-large-scale-fish-dataset"
    )
    print("Kagglehub returned:", path)

    # 2) if it's a zip, unzip it here
    if os.path.isfile(path) and path.endswith(".zip"):
        print("Unzipping zip file…")
        with zipfile.ZipFile(path, "r") as zf:
            zf.extractall(dest_dir)
        raw_root = os.path.join(dest_dir, "Fish_Dataset", "Fish_Dataset")
    # 3) if it's already a directory, just copy it into your local data folder
    elif os.path.isdir(path):
        print("Detected directory — copying into local data folder…")
        # the dataset cache is at path, so inside you'll find Fish_Dataset/
        cache_folder = os.path.join(path, "Fish_Dataset", "Fish_Dataset")
        raw_root = os.path.join(dest_dir, "Fish_Dataset", "Fish_Dataset")
        if not os.path.exists(raw_root):
            shutil.copytree(cache_folder, raw_root)
    else:
        raise RuntimeError(f"Unexpected return from kagglehub: {path}")

    print("Raw images ready at:", raw_root)
    return raw_root

if __name__ == "__main__":
    DATA_DIR = download_fish_dataset()
    print("Point your training script at:", DATA_DIR)
