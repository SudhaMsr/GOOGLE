import cv2
import pytesseract
import pyttsx3

# Configure Tesseract OCR path (update this with your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

class BlindAssistant:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.yolo_net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

    def start_assistant(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Extract text from the frame
            extracted_text = self.extract_text_from_frame(frame)

            # Detect objects in the frame
            objects_detected = self.detect_objects(frame)

            if objects_detected:
                # Convert object results to text
                objects_text = self.format_object_results(objects_detected)

                # Combine extracted text and object text
                final_text = f"{extracted_text}. {objects_text}" if extracted_text else objects_text
            else:
                final_text = extracted_text

            if final_text:
                # Convert final text to audio
                self.convert_text_to_audio(final_text)

            # Display the frame with text and object detection (for visualization purposes)
            cv2.putText(frame, final_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Blind Assistant', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close all OpenCV windows
        self.release_camera()

    def extract_text_from_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text

    def detect_objects(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
        self.yolo_net.setInput(blob)
        layer_names = self.yolo_net.getLayerNames()
        output_layers_indices = self.yolo_net.getUnconnectedOutLayers()
        output_layers = [layer_names[i[0] - 1] for i in output_layers_indices]

        outputs = self.yolo_net.forward(output_layers)

        objects_detected = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = scores.argmax()
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * frame.shape[1])
                    center_y = int(detection[1] * frame.shape[0])
                    w = int(detection[2] * frame.shape[1])
                    h = int(detection[3] * frame.shape[0])
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    objects_detected.append((self.classes[class_id], confidence, (x, y, w, h)))
        return objects_detected

    def format_object_results(self, objects_detected):
        objects_text = ""
        for obj, confidence, _ in objects_detected:
            objects_text += f"{obj} (Confidence: {confidence:.2f}), "
        return objects_text[:-2]

    def convert_text_to_audio(self, text):
        engine.say(text)
        engine.runAndWait()

    def release_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    blind_assistant = BlindAssistant()
    blind_assistant.start_assistant()
