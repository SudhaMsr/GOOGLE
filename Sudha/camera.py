
import cv2
import pytesseract
import pyttsx3

# Configure Tesseract OCR path (update this with your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

def extract_text_from_frame(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use Tesseract OCR to extract text
    text = pytesseract.image_to_string(gray)

    return text

def convert_text_to_audio(text):
    # Use Text-to-Speech engine to convert text to audio
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Open the camera (use 0 for the default camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Extract text from the frame
        extracted_text = extract_text_from_frame(frame)

        # Convert extracted text to audio
        convert_text_to_audio(extracted_text)

        # Display the frame with text (for visualization purposes)
        cv2.putText(frame, extracted_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Camera Feed', frame)

        # Provide voice instructions for improved accessibility
        voice_instructions = "Press 'q' to exit the program."
        convert_text_to_audio(voice_instructions)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
