import os
import shutil

def post_img(img, url):
    if not os.path.exists(img):
        print(f"Source directory '{img}' does not exist.")
        return

    if not os.path.exists(url):
        os.makedirs(url)
        print(f"Destination directory '{url}' created.")
    files = os.listdir(img)

    for file in files:
        if file.lower().endswith('.jpg'):
            source_file = os.path.join(img, file)
            destination_file = os.path.join(url, file)
            shutil.move(source_file, destination_file)
            print(f"Moved '{file}' to '{url}'.")