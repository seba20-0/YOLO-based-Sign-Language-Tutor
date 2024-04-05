from ultralytics import YOLO
import cv2
import math

def RunYOLOWebcam(path_x):
  # start webcam
  cap = cv2.VideoCapture(path_x)
  frame_width=int(cap.get(3))
  frame_height=int(cap.get(4))

  # model
  model = YOLO("best.pt")

  # object classes
  classNames = [""] * 26  # Create an array with 26 empty strings

  for i in range(26):
    classNames[i] = chr(65 + i)  # Fill the array with uppercase letters (A-Z)

    while True:
        success, img = cap.read()
        results=model(img,stream=True)
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confidence
                confidence = math.ceil((box.conf[0]*100))/100

                # class name
                cls = int(box.cls[0])
                class_name=classNames[cls]
                label=f'{class_name}{confidence}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3

                color = (85,45,255)
                if confidence>0.5:
                    cv2.rectangle(img, (x1,y1), (x2,y2), color,3)
                    cv2.rectangle(img, (x1,y1), c2, color, -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)

        yield img
    cv2.destroyAllWindows()