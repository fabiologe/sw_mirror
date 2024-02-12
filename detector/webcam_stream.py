import cv2
import argparse
import time
from ultralytics import YOLO
import supervision as sv
import numpy as np
from detector.img_stream import count_img
from detector.utils import save_image
n_img = 4



# passing console args for supervision 
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[640, 480], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args
#Set Polygon for specific webcam area which should be monitored 
ZONE_POLYGON = np.array([
    [0, 0],
    [0.8, 0],
    [0.8, 1],
    [0, 1]
])

def detector():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=1,
        text_thickness=1,
        text_scale=1
    )

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    img_saved = 0 
    folder_path = "detector/img"
    while True:
            ret, frame = cap.read()

            result = model(frame, agnostic_nms=True)[0]
    
            detections = sv.Detections.from_yolov8(result)
            detections = detections[(detections.class_id == 0) & (detections.confidence > 0.95)]

            person_inside = False
            frame = box_annotator.annotate(
                scene=frame, 
                detections=detections
            )  
            for class_id in detections.class_id:
                if class_id == 0 : 
                    print("Hurray Person")
                    person_inside = True
                    break
            if person_inside == True:
                    save_image(folder_path, frame)
                    img_saved += 1
                    if img_saved >= 4:
                         print("Enough Images")
                         break  
            zone.trigger(detections=detections)
            cv2.imshow("yolov8", frame)
            if (cv2.waitKey(30) == 27):
                break    


# num_img:  counted from folde
# n_img: limiter for outgoing images     
def detector_handler(path, n_img):
    while True:
        num_img = count_img(path)
        if num_img >= n_img:
            print("ENDE ChECK FOLDER")
            break
        detector()
    

