
import cv2
import numpy as np

# Load YOLO
net = cv2.dnn.readNet("path/to/yolov3.weights", "path/to/yolov3.cfg")

# Load COCO names (classes)
classes = []
with open("path/to/coco.names", "r") as f:
    classes = [line.strip() for line in f]

# Load video file
video_path = "path/to/your/video/file.mp4"
cap = cv2.VideoCapture(video_path)

# List to store deteced objects with timestamps
detected_objects = []

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        break

    # Get frame dimensions
    height, width, _ = frame.shape

    # Create a blob from the frame
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Set the input blob for the network
    net.setInput(blob)

    # Run forward pass to get output from the output layers
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Get current timestamp
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC)

    for out in outs:
        for detection in out:
            # Process the detected objects
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > 0.5:  # Confidence threshold
                        # Get the coordinates of the bounding box
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Draw a bounding box
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Display the class label and confidence
                        label = f"{classes[class_id]}: {confidence:.2f}"
                        cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        # Add detected object and timestamp to the list
                        detected_objects.append({
                            "time": current_time,
                            "class_id": class_id,
                            "lable": classes[class_id],
                            "confidence": confidence,
                            "bounding_box": (x, y, w, h)
                        })

    # Display the resulting frame
    cv2.imshow('Object Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
