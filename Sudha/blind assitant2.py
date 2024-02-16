import cv2
import pytesseract
import pyttsx3

# Configure Tesseract OCR path (update this with your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

class BlindAssistant:
    def __init__(self):
        # Load YOLO model
        self.yolo_net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")
        self.object_classes = []
        with open("coco.names", "r") as f:
            self.object_classes = [line.strip() for line in f.readlines()]

    def detect_objects(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
        self.yolo_net.setInput(blob)
        outputs = self.yolo_net.forward(self.get_output_layers())
        
        object_results = []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = int(np.argmax(scores))
                confidence = float(scores[class_id])
                if confidence > 0.5:
                    center_x = int(detection[0] * frame.shape[1])
                    center_y = int(detection[1] * frame.shape[0])
                    w = int(detection[2] * frame.shape[1])
                    h = int(detection[3] * frame.shape[0])
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    object_results.append((self.object_classes[class_id], confidence, (x, y, w, h)))
        return object_results

    def get_output_layers(self):
        layer_names = self.yolo_net.getLayerNames()
        return [layer_names[i[0] - 1] for i in self.yolo_net.getUnconnectedOutLayers()]

    def convert_text_to_audio(self, text):
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    blind_assistant = BlindAssistant()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Detect objects in the frame
        objects_detected = blind_assistant.detect_objects(frame)

        # Format object detection results as text
        object_text = ""
        for obj, confidence, _ in objects_detected:
            object_text += f"{obj} (Confidence: {confidence:.2f}), "

        # Extract text from the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        extracted_text = pytesseract.image_to_string(gray)

        # Combine object detection text and extracted text
        final_text = f"{extracted_text}. {object_text}" if extracted_text else object_text

        # Convert final text to audio
        blind_assistant.convert_text_to_audio(final_text)

        # Display the frame with text and object detection (for visualization purposes)
        cv2.putText(frame, final_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Camera Feed', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
