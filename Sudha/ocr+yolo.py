import cv2
import pytesseract
import pyttsx3
from ultralytics import YOLO

# Initialize the YOLO model
model = YOLO("Pretrained_networks/yolov8n.pt")

# Initialize the OCR engine
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# Function to perform object detection and text extraction
def detect_objects_and_extract_text(frame):
    # Perform object detection using YOLO
    boxes = model(frame)[0].boxes

    # Perform text extraction using Tesseract OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray)

    # Convert extracted text to audio
    engine.say(extracted_text)
    engine.runAndWait()

    # Draw bounding boxes on the frame for detected objects
    for b in boxes:
        c = b.xywh[0].tolist()
        x, y, w, h = int(c[0]), int(c[1]), int(c[2]) // 2, int(c[3]) // 2
        cv2.rectangle(frame, (x - w, y - h), (x + w, y + h), (0, 255, 0), 2)

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
