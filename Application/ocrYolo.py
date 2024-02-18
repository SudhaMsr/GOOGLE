import time

import pytesseract
import pyttsx3
from ultralytics import YOLO
from annotate_realtime import realTimeAnnotate

# Initialize the YOLO model
model = YOLO("Pretrained_networks/detection/detect/train2/weights/best.pt")

classes = ['tree', 'red_light', 'green_light', 'crosswalk', 'blind_road', 'sign', 'person', 'bicycle', 'bus',
           'truck', 'car', 'motorcycle', 'reflective_cone', 'ashcan', 'warning_column', 'roadblock', 'pole', 'dog',
           'tricycle', 'fire_hydrant']

# Initialize the OCR engine
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# global value objectDict, key: track_id, value: Prompt
promptDict = {}

FRAME_WIDTH = None

# Function to perform object detection and text extraction
def detect_objects_and_extract_text(frame):
    lastTime = time.time()
    global FRAME_WIDTH
    if FRAME_WIDTH is None:
        FRAME_WIDTH = frame.shape[1]


    # Perform object detection using YOLO
    tracks, distances, speeds = realTimeAnnotate(frame)
    # boxes = model(frame)[0].boxes

    # Perform text extraction using Tesseract OCR
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # extracted_text = pytesseract.image_to_string(gray)
    #
    # # Convert extracted text to audio
    # threading.Thread(target=say, args=(extracted_text,)).start()

    # Convert the information to text prompt
    # speeding vehicles, traffic light, blind_road, crosswalk, close people, close pole

    tempPrompts = {}
    for track in tracks:
        tr = track.tolist()
        # find the centre_x of the image
        x_centre = (tr[0] + tr[2]) / 2
        tr_id = tr[4]
        name = classes[tr[5]]
        if x_centre < FRAME_WIDTH / 3:
            directionText = "front left"
        elif x_centre > FRAME_WIDTH / 3 * 2:
            directionText = "front right"
        else:
            directionText = "front"


        match name:
            case 'car':
                if speeds[tr_id] > 7 and distances[tr_id] < 20:
                    tempPrompts[name] = Prompt(0, f"speeding car at {directionText}, {distances[tr_id]} meters away.")
            case 'truck':
                if speeds[tr_id] > 5 and distances[tr_id] < 20:
                    tempPrompts[name] = Prompt(0, f"speeding truck at {directionText}, {distances[tr_id]} meters away.")
            case 'bus':
                if speeds[tr_id] > 5 and distances[tr_id] < 20:
                    tempPrompts[name] = Prompt(0, f"speeding bus at {directionText}, {distances[tr_id]} meters away.")
            case 'red_light':
                tempPrompts[name] = Prompt(1, f"red light at {directionText}.")
            case 'green_light':
                tempPrompts[name] = Prompt(2, f"green light at {directionText}.")
            case 'blind_road':
                tempPrompts[name] = Prompt(2, f"blind road at {directionText}.")
            case 'crosswalk':
                tempPrompts[name] = Prompt(3, f"crosswalk at {directionText}.")
            case 'person':
                if distances[tr_id] < 5:
                    tempPrompts[name] = Prompt(4, f"person at {directionText}.")
            case 'pole':
                if distances[tr_id] < 3:
                    tempPrompts[name] = Prompt(5, f"pole at {directionText}.")

    # find the most important prompt
    if not tempPrompts:
        return None

    promptId = min(tempPrompts, key=lambda k: tempPrompts[k].priority)
    decayPrompts(time.time() - lastTime)
    return inputDict(promptId, tempPrompts[promptId])


def inputDict(track_id, prompt):
    # input the prompts into dictionary, output text prompt for this frame (nullable)
    if track_id in promptDict.keys() and prompt.priority <= promptDict[track_id].priority:
        return None
    promptDict[track_id] = prompt
    return prompt.textPrompt


def decayPrompts(timeInterval):
    ids_removed = []
    for track_id in promptDict.keys():
        promptDict[track_id].decay(timeInterval)
        print(promptDict[track_id].forget)
        if promptDict[track_id].forget <= 0:
            ids_removed.append(track_id)
    for track_id in ids_removed:
        del promptDict[track_id]


# Define the text prompt class:
class Prompt:
    def __init__(self, priority, textPrompt):
        self.priority = priority
        self.textPrompt = textPrompt
        self.forget = 5

    def decay(self, timeInterval):
        self.forget -= timeInterval
