import cv2
import pytesseract
import pyttsx3
from ultralytics import YOLO
from Forest.annotate_realtime import realTimeAnnotate

# Initialize the YOLO model
model = YOLO("Pretrained_networks/yolov8n.pt")

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

    # Perform text extraction using Tesseract OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray)

    # Convert extracted text to audio
    engine.say(extracted_text)
    engine.runAndWait()

    # Draw bounding boxes on the frame for detected objects
    # for b in boxes:
    #     c = b.xywh[0].tolist()
    #     x, y, w, h = int(c[0]), int(c[1]), int(c[2]) // 2, int(c[3]) // 2
    #     cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), (0, 255, 0), 2)

    for track in tracks:
        tr = track.tolist()
        x1, y1, x2, y2, name = int(tr[0]), int(tr[1]), int(tr[2]), int(tr[3]), model.names[int(tr[5])]
        tr_id = tr[4]
        name = classes[tr[5]]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 225), 2)
        cv2.putText(frame, f"ID: {tr_id}, {name}, {distances[tr_id] if name in ['car', 'truck', 'bus', 'person'] else ''}m", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)

    # Display the frame
    cv2.imshow('Object Detection and Text Extraction', frame)

# Initialize the video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection and text extraction on the frame
    detect_objects_and_extract_text(frame)

    # Quitting
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
