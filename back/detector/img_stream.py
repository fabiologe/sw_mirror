import os
import cv2
import shutil
import supervision as sv
from ultralytics import YOLO
from detector.utils import save_image

def count_img(img_folder):

    if not os.path.isdir(img_folder):
        print("Error: The specified directory does not exist.")
        return -1
    files = os.listdir(img_folder)


    img_files = [file for file in files if file.endswith(('.jpg'))]

    num_img = len(img_files)

    return num_img  
            

def delete_all_images(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                os.remove(os.path.join(root, file))

            
def static_detector(folder_path, save_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg')):
            img_path = os.path.join(folder_path, filename)
            model = YOLO("yolov8l.pt")
            image = cv2.imread(img_path)
            result = model(image)[0]
            detections = sv.Detections.from_yolov8(result)
            detections = detections[(detections.class_id != 0)]

            # both not implemented in sv == 0.15.0
            '''polygon_annotator = sv.PolygonAnnotator()
            annotated_frame = polygon_annotator.annotate(
                             scene=image.copy(),
                                detections=detections
                                )'''
            '''mask_annotator = sv.MaskAnnotator()
            annotated_frame = mask_annotator.annotate(
              scene=image.copy(),
	        detections=detections 
            )'''
            blur_annotator = sv.BlurAnnotator(
                kernel_size= 10
            )


            annotated_frame = blur_annotator.annotate(
	        scene=image.copy(),
	        detections=detections
            )
            save_image(save_path, frame= annotated_frame)
            cv2.imshow("yolov8", annotated_frame)
    delete_all_images(folder_path)
    return
            




