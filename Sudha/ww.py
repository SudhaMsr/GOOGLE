import cv2
from PIL import Image, ImageTk
import pytesseract
import pyttsx3
import tkinter as tk
from tkinter import ttk

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

engine = pyttsx3.init()

def extract_text_from_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def convert_text_to_audio(text):
    engine.say(text)
    engine.runAndWait()

def start_processing():
    cap = cv2.VideoCapture(0)

    def process_frame():
        ret, frame = cap.read()
        extracted_text = extract_text_from_frame(frame)
        convert_text_to_audio(extracted_text)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Schedule the function to be called again after 100 milliseconds
        app.after(100, process_frame)

    # Start the processing loop
    process_frame()

app = tk.Tk()
app.title("Text-to-Speech App")

video_label = ttk.Label(app)
video_label.pack()

start_button = ttk.Button(app, text="Start", command=start_processing)
start_button.pack()

exit_button = ttk.Button(app, text="Exit", command=app.destroy)
exit_button.pack()

app.mainloop()

