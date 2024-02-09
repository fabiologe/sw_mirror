import cv2
import argparse
import time
from ultralytics import YOLO
import supervision as sv
import numpy as np


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

    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]
        #print(result)
        detections = sv.Detections.from_yolov8(result)
        detections = detections[detections.class_id == 0]

        #print(detections)
        person_inside = False
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        print(labels)
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections 
            #labels=labels
        )
        for class_id in detections.class_id:

            if class_id == 0 : 
                print("Hurray Person")
                person_inside = True
                break
        if person_inside == True:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            cv2.imwrite("detector/img/person_detected_{}.jpg".format(timestamp), frame)
        
        zone.trigger(detections=detections)
        

        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            break

