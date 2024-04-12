import tensorflow as tf
from transformers import AutoProcessor, TFBlipForQuestionAnswering, DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import numpy as np
import torch

def get_image_caption(image_path):
    """
    Generates a short caption for the provided image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: A string representing the caption for the image.
    """
    image = Image.open(image_path).convert('RGB')
    image = np.array(image)  # Convert PIL Image to numpy array

    model_name = "Salesforce/blip-image-captioning-large"

    model = TFBlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

    processor = AutoProcessor.from_pretrained("Salesforce/blip-vqa-base")
    text = 'Describe the img'

    # Convert the image data to TensorFlow tensor
    image_tensor = tf.convert_to_tensor(image)

    inputs = processor(images=image_tensor, text=text, return_tensors='tf')
    output = model.generate(**inputs)

    caption = processor.decode(output[0], skip_special_tokens=True)

    return caption

def detect_objects(image_path):
    """
    Detects objects in the provided image.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: A string with all the detected objects. Each object as '[x1, x2, y1, y2, class_name, confindence_score]'.
    """
    image = Image.open(image_path).convert('RGB')

    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.9
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    detections = ""
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        detections += '[{}, {}, {}, {}]'.format(int(box[0]), int(box[1]), int(box[2]), int(box[3]))
        detections += ' {}'.format(model.config.id2label[int(label)])
        detections += ' {}\n'.format(float(score))

    return detections


if __name__ == '__main__':
    image_path = '/home/fabioiologe/Documents/code/sw_mirror/back/img/guy_with_chick.jpg'
    detections = detect_objects(image_path)
    description = get_image_caption(image_path)
    print(detections)
    print(description)
