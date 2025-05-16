import os
import shutil
import re


# Path to the folder containing 1000 images
image_folder_action = "photo_extract/Action_cons_files"
output_folder_action = "photo_extract/action_images"

image_folder_emotion = "photo_extract/Emotion_cons_files"
output_folder_emotion = "photo_extract/emotion_images"

def create_batches(image_folder, output_folder):
    """
    Create 5 batches of images from the specified folder and copy them into separate folders.
    """
    # Create 5 batch folders
    batch_size = 200
    for batch_num in range(1, 6):
        batch_folder = os.path.join(output_folder, f"batch_{batch_num}")
        os.makedirs(batch_folder, exist_ok=True)

    # Get all image files and sort them numerically
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))])

    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else -1

    image_files.sort(key=extract_number)

    # Distribute images into batches
    for i, file in enumerate(image_files):
        batch_num = (i // batch_size) + 1
        if batch_num > 5:  # Ensure no more than 5 batches
            break
        source_path = os.path.join(image_folder, file)
        destination_path = os.path.join(output_folder, f"batch_{batch_num}", file)
        shutil.copy(source_path, destination_path)

    print("Images have been copied into 5 batches.")

if __name__ == "__main__":
    # Create output folders if they don't exist
    os.makedirs(output_folder_action, exist_ok=True)
    os.makedirs(output_folder_emotion, exist_ok=True)

    # Create batches for action images
    create_batches(image_folder_action, output_folder_action)

    # Create batches for emotion images
    create_batches(image_folder_emotion, output_folder_emotion)