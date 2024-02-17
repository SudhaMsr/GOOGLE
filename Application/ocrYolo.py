import cv2
import pytesseract
import pyttsx3
from ultralytics import YOLO
from annotate_realtime import realTimeAnnotate
import threading

# Initialize the YOLO model
model = YOLO("Pretrained_networks/detection/detect/train2/weights/best.pt")

classes = ['tree', 'red_light', 'green_light', 'crosswalk', 'blind_road', 'sign', 'person', 'bicycle', 'bus',
           'truck', 'car', 'motorcycle', 'reflective_cone', 'ashcan', 'warning_column', 'roadblock', 'pole', 'dog',
           'tricycle', 'fire_hydrant']

# Initialize the OCR engine
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# Function to perform object detection and text extraction
def detect_objects_and_extract_text(frame):

    # Perform object detection using YOLO
    tracks, distances, speeds = realTimeAnnotate(frame)
    # boxes = model(frame)[0].boxes
    print("Processed")

    # Perform text extraction using Tesseract OCR
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # extracted_text = pytesseract.image_to_string(gray)
    #
    # # Convert extracted text to audio
    # threading.Thread(target=say, args=(extracted_text,)).start()

    for track in tracks:
        tr = track.tolist()
        x1, y1, x2, y2, name = int(tr[0]), int(tr[1]), int(tr[2]), int(tr[3]), model.names[int(tr[5])]
        tr_id = tr[4]
        name = classes[tr[5]]
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 225), 2)
        # cv2.putText(frame, f"ID: {tr_id}, {name}, {distances[tr_id] if name in ['car', 'truck', 'bus', 'person'] else ''}m", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)

    # Convert the information to text prompt
    textPrompt = ""
    
    return textPrompt


def speak(extracted_text):
    threading.Thread(target=say, args=(extracted_text,)).start()


def say(extracted_text):
    engine.say(extracted_text)
    engine.runAndWait()


# Define three classes: vehicle, person, staticObject