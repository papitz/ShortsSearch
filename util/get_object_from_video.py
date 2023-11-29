#!/usr/bin/env python
# get_ipython().system(' pip3 install opencv-python numpy ultralytics')

import cv2
import numpy as np
from ultralytics import YOLO
# import json


## Function to extract object names
def get_list_of_objects(result, min_confidence):
    objectIndices = result[0].probs.top5
    confidences = result[0].probs.top5conf
    objects = []
    # Go through all predictions and only collect the ones with high confidence
    for i in range(0, len(objectIndices)):
        if confidences[i] > min_confidence:
            objects.append(result[0].names[objectIndices[i]])
    return objects


## Function to get objects from single image
def get_objects_from_frame(model, frame, min_confidence):
    result = model.predict(source=frame, stream=False, verbose=False)
    return get_list_of_objects(result, min_confidence)


## Get all frames from a video and find objects
def detect_objects_in_video(video_path, model, min_confidence):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file")
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Extract every fifth frame
    frame_interval = 5
    detected_objects = set()
    for frame_number in range(0, frame_count, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if not ret:
            print(f"Error reading frame {frame_number}")
            break

        # Call the provided function with the extracted frame
        for detected_object in get_objects_from_frame(model, frame, min_confidence):
            detected_objects.add(detected_object)

    cap.release()
    cv2.destroyAllWindows()
    # Convert the set of detected objects to a list
    detected_objects_list = list(detected_objects)
    return detected_objects
