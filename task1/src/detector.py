import torch
import cv2
from ultralytics import YOLO
import os

class PlayerDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame)
        detections = []
        for r in results:
            boxes = r.boxes.cpu().numpy() if hasattr(r, 'boxes') else []
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = r.names[cls] if hasattr(r, 'names') else str(cls)
                detections.append({
                    'bbox': [float(x1), float(y1), float(x2), float(y2)],
                    'conf': float(conf),
                    'cls': cls,
                    'label': label
                })
        return detections
