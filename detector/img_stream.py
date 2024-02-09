import supervision as sv

img_stream = "detector/img"

polygon_annotator = sv.PolygonAnnotator()
annotated_frame = polygon_annotator.annotate(
    scene=image.copy(),
    detections=detections
)