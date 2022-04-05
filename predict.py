import numpy as np
import tensorflow_hub as hub
import cv2

from label_map import label_map

def load_model():
    print("loading model...")
    hub_model = hub.load("https://tfhub.dev/tensorflow/retinanet/resnet50_v1_fpn_640x640/1")
    print('model loaded!')

    return hub_model

def predict_image(img, model):
    img_prep = [img]
    image_width = img.shape[1]
    image_height = img.shape[0]

    # Run inference
    print("predicting...")
    results = model(img_prep)
    print("prediction done!")

    # Prepare returned data from results
    classes = results['detection_classes'][0].numpy().astype(int)
    scores = results['detection_scores'][0]
    bounding_boxes = results['detection_boxes'][0]

    # Turn the data into something more readable
    objects = []
    for index, score in enumerate(scores):
        label = "?"

        if classes[index] in label_map.keys():
            # Get label from label map
            label = label_map[classes[index]]['name']
        else:
            # Skip
            continue

        # Boundings box of the object
        y_min, x_min, y_max, x_max = bounding_boxes[index]

        # Push to array
        objects.append({
            "label": label,
            "score": score.numpy(),
            "top_left_corner": (
                int(x_min * image_width),
                int(y_min * image_height)
            ),
            "bottom_right_corner": (
                int(x_max * image_width),
                int(y_max * image_height)
            )
        })
    
    return objects

def annotate_image(img, preds, color=(0, 255, 0)):
    img_annotated = np.copy(img)

    # Draw a rect and text for each prediction if it has a score over 50%
    for pred in preds:
        if pred["score"] > 0.5:
            score = round(pred['score'] * 100)
            img_annotated = cv2.rectangle(img_annotated, pred['top_left_corner'], pred['bottom_right_corner'], color, 2)
            cv2.putText(img_annotated, f"{pred['label']} {score}%", pred["top_left_corner"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    return img_annotated
