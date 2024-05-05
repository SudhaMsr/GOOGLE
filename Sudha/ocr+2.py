import cv2
import pytesseract

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize the OCR engine
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Perform OCR on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(gray)

    # Display the frame with extracted text
    cv2.putText(frame, extracted_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Real-Time OCR', frame)

    # Exit on 'q' key press
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
