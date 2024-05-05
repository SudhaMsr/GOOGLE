from ultralytics import YOLO
import yaml
import json
import numpy as np
import torch

model = YOLO("Pretrained_networks/yolov8n.pt")
print(torch.cuda.get_device_name(0))

with open('../../Forest/datasets/WOTR_yolo/wotr.yaml', 'r') as yaml_file:
    dataset = yaml_file.read()

model.train(data='datasets/WOTR_yolo/wotr.yaml', epochs=100, device=torch.device(0))
