from ultralytics import YOLO
import cv2
from Public.utilities import drawBoxes
from annotate_realtime import realTimeAnnotate


capture = cv2.VideoCapture(0)
while capture.isOpened():
    _, frame = capture.read()

    # get the annotations of frame
    tracks, distances, speeds = realTimeAnnotate(frame)

    # quitting
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
