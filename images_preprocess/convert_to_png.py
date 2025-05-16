from PIL import Image
import base64
import os

def convert_to_png(image_path):
    try:
        img = Image.open(image_path)
        if img.format != "PNG":
            print(f"Detected format: {img.format}. Converting to PNG.")
            temp_path = image_path
            img.save(temp_path, "PNG")
            image_path = temp_path
        else:
            print("Image is already PNG")
    except Exception as e:
        raise ValueError(f"Invalid image file: {e}")



for folder in os.listdir(r"C:\VScode\Construction_CV\photo_extract"):
    if folder == "action_images":
        for folder in os.listdir(r"C:\VScode\Construction_CV\photo_extract\action_images"):
            if folder.endswith(".zip"):
                continue
            for file in os.listdir(os.path.join(r"C:\VScode\Construction_CV\photo_extract\action_images",folder)):
                if file.endswith(".png"):
                    image_paths_input = os.path.join(fr"C:\VScode\Construction_CV\photo_extract\action_images\{folder}", file)
                    convert_to_png(image_paths_input)
    elif folder == "emotion_images":
        for folder in os.listdir(r"C:\VScode\Construction_CV\photo_extract\emotion_images"):
            if folder.endswith(".zip"):
                continue
            for file in os.listdir(os.path.join(r"C:\VScode\Construction_CV\photo_extract\emotion_images",folder)):
                if file.endswith(".png"):
                    image_paths_input = os.path.join(fr"C:\VScode\Construction_CV\photo_extract\emotion_images\{folder}", file)
                    convert_to_png(image_paths_input)
                


