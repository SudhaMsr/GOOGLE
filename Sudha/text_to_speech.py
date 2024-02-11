import tkinter as tk
import cv2
import pytesseract
import pyttsx3

# Configure Tesseract OCR path (update this with your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

class BlindAssistanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blind Assistance App")

        self.label = tk.Label(root, text="Blind Assistance App")
        self.label.pack()

        self.btn_start = tk.Button(root, text="Start", command=self.open_camera)
        self.btn_start.pack()

        self.cap = None

    def open_camera(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Extract text from the frame
            extracted_text = self.extract_text_from_frame(frame)

            if extracted_text:
                # Convert extracted text to audio
                self.convert_text_to_audio(extracted_text)

            # Display the frame with text (for visualization purposes)
            cv2.putText(frame, extracted_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Camera Feed', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close all OpenCV windows
        self.cap.release()
        cv2.destroyAllWindows()

    def extract_text_from_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text

    def convert_text_to_audio(self, text):
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlindAssistanceApp(root)
    root.mainloop()