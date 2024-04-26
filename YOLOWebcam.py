from ultralytics import YOLO
import cv2
import math

def RunYOLOWebcam(path_x):
    # Start webcam
    #global class_name
    cap = cv2.VideoCapture(path_x)
    desired_width = 540
    desired_height = 300
    # Model
    model = YOLO("best.pt")

    # Object classes
    classNames = [""] * 26  # Create an array with 26 empty strings
    for i in range(26):
        classNames[i] = chr(65 + i)  # Fill the array with uppercase letters (A-Z)
    
    while True:
        success, img = cap.read()
        if not success:
            break

        # Perform YOLO detection on the original image
        results = model(img, stream=True)

        # Save bounding box coordinates
        bounding_boxes = []
        detected_classes = []
        confidence_scores = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxyn[0]
                bounding_boxes.append((x1, y1, x2, y2))
                detected_class = classNames[int(box.cls[0])]
                detected_classes.append(detected_class)
                confidence_scores.append(box.conf[0])

        # Resize the image to the desired resolution
        img_resized = cv2.resize(img, (desired_width, desired_height))

        # Resize the bounding boxes to match the resized image
        resized_bounding_boxes = []
        for box in bounding_boxes:
            x1, y1, x2, y2 = box
            x1_resized, y1_resized, x2_resized, y2_resized = int(x1 * desired_width), \
                                                            int(y1 * desired_height), \
                                                            int(x2 * desired_width), \
                                                            int(y2 * desired_height)
            resized_bounding_boxes.append((x1_resized, y1_resized, x2_resized, y2_resized))
            
        # Draw bounding boxes on the resized image
        for box, detected_class, confidence_score in zip(resized_bounding_boxes, detected_classes ,  confidence_scores):
            x1, y1, x2, y2 = box
            # Calculate confidence score based on detected_class
            label = f'{detected_class} {confidence_score:.2f}'  # Concatenate class name and confidence score
            cv2.rectangle(img_resized, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(img_resized, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)


        #class_name = detected_class
        # Resize the image to the desired resolution
        #img_resized = cv2.resize(img, (desired_width, desired_height))
        
        # Draw bounding boxes on the resized image
        #for box in bounding_boxes:
         #   x1, y1, x2, y2 = box
          #  cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        
        

        yield img_resized,detected_classes

    cv2.destroyAllWindows()