import subprocess
import os
from PIL import Image
def compress_png_lossy(png_file):
    # Run pngquant with a specified quality range (0–100)
    try:
            subprocess.run(
                ['pngquant', '--quality=50-60', '--ext', '.png', '--force', png_file],
                check=True
            )
            print(f"Compressed: {png_file}")
    except subprocess.CalledProcessError as e:
            if e.returncode == 99:
                print(f"Already optimized or cannot compress: {png_file}")
            else:
                print(f"Failed to compress: {png_file}. Error: {e}")

# Example usage
# input_image_path = r"C:\VScode\Construction_CV\photo_extract\emotion_images\batch_1\image001.png"
# output_image_path = r"C:\VScode\Construction_CV\photo_extract\emotion_images\batch_1\image001_compressed.png"
# compress_png_lossy(input_image_path, output_image_path)

for folder in os.listdir(r"C:\VScode\Construction_CV\photo_extract"):
    if folder == "action_images":
        for folder in os.listdir(r"C:\VScode\Construction_CV\photo_extract\action_images"):
            if folder.endswith(".zip"):
                continue
            for file in os.listdir(os.path.join(r"C:\VScode\Construction_CV\photo_extract\action_images",folder)):
                if file.endswith(".png"):
                    image_paths_input = os.path.join(fr"C:\VScode\Construction_CV\photo_extract\action_images\{folder}", file)
                    compress_png_lossy(image_paths_input)
    elif folder == "emotion_images":
        for folder in os.listdir(r"C:\VScode\Construction_CV\photo_extract\emotion_images"):
            if folder.endswith(".zip"):
                continue
            for file in os.listdir(os.path.join(r"C:\VScode\Construction_CV\photo_extract\emotion_images",folder)):
                if file.endswith(".png"):
                    image_paths_input = os.path.join(fr"C:\VScode\Construction_CV\photo_extract\emotion_images\{folder}", file)
                    compress_png_lossy(image_paths_input)