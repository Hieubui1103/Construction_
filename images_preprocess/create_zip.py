import os
import zipfile

def create_zip_for_batches(directory, output_dir):
    """
    Create a zip file for each batch folder in the given directory.

    Args:
        directory (str): Path to the directory containing batch folders.
        output_dir (str): Path to the directory where zip files will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for batch_folder in os.listdir(directory):
        batch_path = os.path.join(directory, batch_folder)
        if os.path.isdir(batch_path):
            zip_file_path = os.path.join(output_dir, f"{batch_folder}.zip")
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(batch_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, batch_path)
                        zipf.write(file_path, arcname)
            print(f"Created: {zip_file_path}")

# Example usage
input_directory_action = "photo_extract/action_images" # Replace with the path to your batch folders
output_directory_action = "photo_extract/action_images"  # Replace with the path to save zip files
input_directory_emotion = "photo_extract/emotion_images" # Replace with the path to your batch folders
output_directory_emotion = "photo_extract/emotion_images"  # Replace with the path to save zip files
create_zip_for_batches(input_directory_emotion, output_directory_emotion)