import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np

person_inside = False

ZONE_POLYGON = np.array([
    [0, 0],
    [0.8, 0],
    [0.8, 1],
    [0, 1]
])


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


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    model = YOLO("yolov8l.pt")

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
    zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
    zone_annotator = sv.PolygonZoneAnnotator(
        zone=zone, 
        color=sv.Color.red(),
        thickness=2,
        text_thickness=4,
        text_scale=2
    )

    while True:
        ret, frame = cap.read()

        result = model(frame, agnostic_nms=True)[0]
        #print(result)
        detections = sv.Detections.from_yolov8(result)
        #print(detections)
        person_inside = False

        for class_id in detections.class_id:
            #print(class_id)

            if class_id == 0 : 
                print("Hurray Person")
                person_inside = True
                break

        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        print(labels)
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )

        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)      
        
        # Define the text and font properties
        text = "Keine Person"
        if person_inside:
            text = "rassist detected"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2  # You can adjust this value to make the text bigger or smaller
        font_thickness = 5
        text_color = (255, 255, 255)  # white color
        background_color = (0, 0, 255)  # red color

        # Get the size of the text
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

        # Calculate the position to place the text at the middle top
        text_x = (frame_width - text_width) // 2
        text_y = text_height + 10  # You can adjust this value for the vertical position
        background_padding = 5
        cv2.rectangle(frame, (text_x - background_padding, text_y - text_height - background_padding),
              (text_x + text_width + background_padding, text_y + baseline + background_padding),
              background_color, cv2.FILLED)
        # Put the text on the frame
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            break


if __name__ == "__main__":
    main()