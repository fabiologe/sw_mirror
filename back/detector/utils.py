import time
import cv2
import os 
import request

def save_image(folder_path, frame):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    img_path = os.path.join(folder_path, "person_detected_{}.jpg".format(timestamp))
    cv2.imwrite(img_path, frame)
    time.sleep(3)
    return img_path


