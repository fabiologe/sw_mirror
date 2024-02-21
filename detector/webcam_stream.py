import cv2
import argparse
import numpy as np
import time
from ultralytics import YOLO
import supervision as sv
from detector.img_stream import count_img
from detector.utils import save_image

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution", default=[640, 480], nargs=2, type=int)
    args = parser.parse_args()
    return args

ZONE_POLYGON = np.array([
    [0, 0],
    [0.8, 0],
    [0.8, 1],
    [0, 1]
])

def save_cropped_image(folder_path, frame, bbox):
    x1, y1, x2, y2 = bbox
    cropped_img = frame[y1:y2, x1:x2]
    filename = f"{folder_path}/person_{int(time.time())}.jpg"
    cv2.imwrite(filename, cropped_img)

def detector():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=1)

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    folder_path = "detector/img"
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)

        for i in range(len(detections.class_id)):
            if detections.class_id[i] == 0 and detections.confidence[i] > 0.95:  # Check for person with high confidence
                bbox = detections.xyxy[i].astype(int)  # Convert bounding box to integer
                save_cropped_image(folder_path, frame, bbox)
                exit()

        zone.trigger(detections=detections)
        cv2.imshow("yolov8", frame)
        if cv2.waitKey(30) == 27:
            break


def detector_handler():
    detector()
            
