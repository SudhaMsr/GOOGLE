import os
import xml.etree.ElementTree as ET
import shutil


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id, file):
    # copy image first
    shutil.copy('WOTR/JPEGImages/%s.jpg' % (image_id), f'WOTR_yolo/images/{file}/%s.jpg' % (image_id))

    in_file = open('WOTR/Annotations/%s.xml' % (image_id))
    out_file = open(f'WOTR_yolo/labels/{file}/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes:
            print("skipped")
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


classes = ['tree', 'red_light', 'green_light', 'crosswalk', 'blind_road', 'sign', 'person', 'bicycle', 'bus',
           'truck', 'car', 'motorcycle', 'reflective_cone', 'ashcan', 'warning_column', 'roadblock', 'pole', 'dog',
           'tricycle', 'fire_hydrant']
os.makedirs('WOTR_yolo/labels/train', exist_ok=True)
os.makedirs('WOTR_yolo/labels/val', exist_ok=True)
os.makedirs('WOTR_yolo/images/train', exist_ok=True)
os.makedirs('WOTR_yolo/images/val', exist_ok=True)
image_ids_train = open('WOTR/ImageSets/Main/train.txt').read().strip().split()
for image_id in image_ids_train:
    convert_annotation(image_id, "train")

image_ids_val = open('WOTR/ImageSets/Main/val.txt').read().strip().split()
for image_id in image_ids_val:
    convert_annotation(image_id, "val")
