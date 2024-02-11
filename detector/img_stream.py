import os
import cv2
import shutil
import supervision as sv

def count_img(img_folder):

    if not os.path.isdir(img_folder):
        print("Error: The specified directory does not exist.")
        return -1
    files = os.listdir(img_folder)


    img_files = [file for file in files if file.endswith(('.jpg'))]

    num_img = len(img_files)

    return num_img  
            

def delete_all_images(img_folder):
    for root, dirs, files in os.walk(img_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                os.remove(os.path.join(root, file))

