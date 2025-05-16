import os
import shutil
from PIL import Image
import imagehash
from tqdm import tqdm

# --- SET THESE ---
input_folder = r"C:\Users\trung\Downloads\output merge.v1i.multiclass\train"  # e.g., "C:/Users/You/Pictures/AllImages"
output_folder = r"C:\Users\trung\Downloads\output merge.v1i.multiclass\train_p1"  # e.g., "C:/Users/You/Pictures/UniqueImages"
# ------------------

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Hash storage
hashes = set()
duplicate_count = 0
unique_count = 0

# Loop through images
for root, dirs, files in os.walk(input_folder):
    for file in tqdm(files, desc="Processing images"):
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    img_hash = imagehash.phash(img)

                if img_hash not in hashes:
                    hashes.add(img_hash)
                    shutil.copy(file_path, os.path.join(output_folder, file))
                    unique_count += 1
                else:
                    duplicate_count += 1
            except Exception as e:
                print(f"Error with {file_path}: {e}")

print(f"\n✅ Done! Unique images: {unique_count}, Duplicates removed: {duplicate_count}")
