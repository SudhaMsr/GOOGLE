import math

import torch
from ultralytics import YOLO
import cv2
from deep_sort_realtime.deepsort_tracker import \
    DeepSort  # https://github.com/levan92/deep_sort_realtime?tab=MIT-1-ov-file
from strongsort.strong_sort import StrongSORT  # https://github.com/kadirnar/strongsort-pip
import time
from pathlib import Path
import keras
import numpy as np

TRACKER_NAME = "strongSORT"

# class for angle_estimator:
# classes = ['tree', 'red_light', 'green_light', 'crosswalk', 'blind_road', 'sign', 'person', 'bicycle', 'bus',
#            'truck', 'car', 'motorcycle', 'reflective_cone', 'ashcan', 'warning_column', 'roadblock', 'pole', 'dog',
#            'tricycle', 'fire_hydrant']

# ========== model initialization ==========
model = YOLO("Pretrained_networks/detection/detect/train2/weights/best.pt")
angle_estimator = keras.models.load_model("Pretrained_networks/angle_model/angle_model.keras")
angle_estimator.load_weights("Pretrained_networks/angle_model/best_weight.h5")
if TRACKER_NAME == "deepSORT":
    tracker = DeepSort(max_age=5,
                       n_init=2,
                       nms_max_overlap=1.0,
                       max_cosine_distance=0.3,
                       nn_budget=None,
                       override_track_class=None,
                       embedder="mobilenet",
                       half=True,
                       bgr=True,
                       embedder_gpu=True,
                       embedder_model_name=None,
                       embedder_wts=None,
                       polygon=False,
                       today=None)
else:
    tracker = StrongSORT(model_weights=Path("Pretrained_networks/Track/osnet_x0_25_market1501.pt"), device='cpu',
                         fp16=False)
# ============================================


# ========== CONSTANTS FOR OBJECTS ==========
# VEHICLES (WIDTH, LENGTH)
CAR_SIZE = (1.82, 4.40)
TRUCK_SIZE = (2.9, 6.9)
BUS_SIZE = (2.55, 12)

# AVERAGE PERSON SHOULDER WIDTH
PERSON_SIZE = 0.46


# FOCAL LENGTH (needs calibration)

def getFocalLength():
    return 683


FOCAL_LENGTH = getFocalLength()


# ============================================


lastDistances = {}
lastTime = time.time()

def realTimeAnnotate(frame):
    boxes = objectsDetection(frame)

    tracks = objectTracking(boxes, frame)
    angles = getAngles(tracks, frame)

    distances = distancesEstimation(tracks, angles)
    speeds = speedsEstimation(distances)

    # cv2.imshow('cam', frame)
    return tracks, distances, speeds


def objectTracking(boxes, frame):
    if not boxes:
        return []

    t = time.time()
    if TRACKER_NAME == "deepSORT":
        # each detection is in the form ([left, top, w, h], confidence, class)
        detections = []
        for box in boxes:
            xyxy = box.xyxy[0]
            xywh = box.xywh[0]
            left, top, width, height, name = xyxy[0], xyxy[1], xywh[2], xywh[3], model.names[int(box.cls)]
            detections.append(([left, top, width, height], box.conf, name))
        tracks = tracker.update_tracks(detections, frame=frame)

        # draw tracks
        for tr in tracks:
            if not tr.is_confirmed():
                continue
            tr_id = tr.track_id
            ltrb = tr.to_ltrb()
            bb = [int(e) for e in ltrb]
            """
            cv2.rectangle(frame, (bb[0], bb[1]), (bb[2], bb[3]), (0, 0, 225), 2)
            cv2.putText(frame, str(tr_id), (bb[0], bb[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)
            """

    else:
        # np.array([x1, y1, x2, y2, track_id, class_id, conf]
        detections = []

        for box in boxes:
            xyxy = box.xyxy[0]
            x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
            dets = [x1, y1, x2, y2, int(box.conf[0]), int(box.cls[0])]
            detections.append(dets)

        tracks = tracker.update(torch.tensor(detections), frame)
        """
        for trnp in tracks:
            tr = trnp.tolist()
            cv2.rectangle(frame, (tr[0], tr[1]), (tr[2], tr[3]), (0, 0, 225), 2)
            cv2.putText(frame, f"{model.names[tr[5]]}{str(tr[4])}", (tr[0], tr[1]), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 225), 2)
        """

    duration = time.time() - t
    # cv2.putText(frame, f"FPS: {1 / duration}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
    return tracks


def objectsDetection(frame):
    model.track()
    boxes = model(frame)[0].boxes
    return boxes


def distancesEstimation(tracks, angles):
    distance = {}

    for track in tracks:
        tr = track.tolist()
        name = model.names[tr[5]]
        id = tr[4]

        # D = W * f / w
        w = abs(tr[2] - tr[0])
        match name:
            case 'car':
                W = getActualWidth(CAR_SIZE, angles[id])
            case 'truck':
                W = getActualWidth(TRUCK_SIZE, angles[id])
            case 'bus':
                W = getActualWidth(BUS_SIZE, angles[id])
            case 'person':
                W = getActualWidth(PERSON_SIZE)
            case _:
                continue

        f = FOCAL_LENGTH

        distance[id] = W * f / w
        print(f"Real Width: {W}, Focal Length: {f}, Object Width in Pixels: {w}, Distance: {distance[id]}")
    return distance


def speedsEstimation(distances):
    global lastDistances
    global lastTime

    speeds = {}
    currTime = time.time()
    for track_id in distances.keys():
        if track_id not in lastDistances.keys():
            continue
        # If the id is in last distances, estimate the speed towards the user
        speeds[track_id] = (lastDistances[track_id] - distances[track_id]) / (currTime - lastTime)

    lastDistances = distances
    lastTime = currTime
    return speeds


def getAngles(tracks, frame):
    vehicles = []

    for track in tracks:
        tr = track.tolist()
        x1, y1, x2, y2, name = int(tr[0]), int(tr[1]), int(tr[2]), int(tr[3]), model.names[int(tr[5])]
        if name in ['car', 'truck', 'bus']:
            vehicles.append(
                np.array(cv2.cvtColor(cv2.resize(frame[y1:y2, x1:x2], (128, 128)), cv2.COLOR_BGR2RGB)) / 255)

    # predict
    if not vehicles:
        return dict()

    predicted = angle_estimator.predict(np.array(vehicles)).tolist()
    angles = {}
    cnt = 0
    for track in tracks:
        tr = track.tolist()
        x1, y1, x2, y2, name, id = int(tr[0]), int(tr[1]), int(tr[2]), int(tr[3]), model.names[int(tr[5])], tr[4]
        if name in ['car', 'truck', 'bus']:
            angles[id] = (predicted[cnt][0] * 360)
            angle = predicted[cnt][0] * 360
            cnt += 1

            """
            # draw
            length = 150
            start_point = ((x1 + x2) // 2, (y1 + y2) // 2)
            # Convert the angle to radians
            angle_rad = np.radians(90 - angle)

            # Calculate the end point
            end_point = (int(start_point[0] - length * np.cos(angle_rad)),
                         int(start_point[1] - length * np.sin(angle_rad)))

            # Draw the arrowed line
            # cv2.arrowedLine(frame, start_point, end_point, (0, 255, 0), thickness=2)
            """

    return angles


def getActualWidth(constSize, angle=None):
    if angle is None:
        return constSize

    xOffset = constSize[0] / 2
    yOffset = constSize[1] / 2
    points = np.array([[xOffset, yOffset], [-xOffset, yOffset], [xOffset, -yOffset], [-xOffset, -yOffset]]).transpose()

    angle_rad = math.radians(angle)
    rot_matrix = np.array([[math.cos(angle_rad), -math.sin(angle_rad)],
                           [math.sin(angle_rad), math.cos(angle_rad)]])

    # transform all points
    transformedPoints = np.matmul(rot_matrix, points).transpose()

    # project onto x-axis to get maximum and minimum
    transformedXs = transformedPoints[:, :-1].squeeze()
    return transformedXs.max() - transformedXs.min()

