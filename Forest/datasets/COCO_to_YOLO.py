import json
import yaml
from ultralytics.data.converter import convert_coco


convert_coco('coco/annotations/', use_segments=False, use_keypoints=False, cls91to80=False)
