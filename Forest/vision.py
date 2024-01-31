from ultralytics import YOLO
import cv2
from Public.utilities import drawBoxes

model = YOLO("Pretrained_networks/yolov8n.pt")

capture = cv2.VideoCapture(0)
while capture.isOpened():
    ret, frame = capture.read()

    boxes = model(frame)[0].boxes
    cv2.imshow('cam', drawBoxes(frame, boxes, model.names))

    # quitting
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
