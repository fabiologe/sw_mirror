import time
import cv2
import os 
from PIL import Image

def compress_jpeg(image_path, output_path, quality=85):
    """
    Compress a JPEG image to reduce its file size.

    Args:
    - image_path (str): Path to the input JPEG image.
    - output_path (str): Path to save the compressed image.
    - quality (int): The quality of the compressed image (0-100, higher is better).

    Returns:
    - None
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Convert to RGB mode if not already in RGB mode
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Compress and save the image
            img.save(output_path, format='JPEG', quality=quality)
    except Exception as e:
        print(f"Error compressing image: {e}")

def save_image(folder_path, frame):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    img_path = os.path.join(folder_path, "person_detected_{}.jpg".format(timestamp))
    cv2.imwrite(img_path, frame)
    time.sleep(3)
    return img_path


