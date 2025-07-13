import numpy as np
from scipy.optimize import linear_sum_assignment
from src.feature_extractor import extract_color_histogram
import cv2
import json

def load_tracking_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def extract_all_features(video_path, tracking_json):
    cap = cv2.VideoCapture(video_path)
    features_by_id = {}
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret or frame_idx >= len(tracking_json):
            break
        frame_data = tracking_json[frame_idx]
        for obj_id, bbox in zip(frame_data['objects'].keys(), frame_data['boxes']):
            hist = extract_color_histogram(frame, bbox)
            if obj_id not in features_by_id:
                features_by_id[obj_id] = []
            features_by_id[obj_id].append(hist)
        frame_idx += 1
    cap.release()
    avg_features = {oid: np.mean(hists, axis=0) for oid, hists in features_by_id.items() if len(hists) > 0}
    return avg_features

def map_players(features_a, features_b):
    ids_a = list(features_a.keys())
    ids_b = list(features_b.keys())
    cost_matrix = np.zeros((len(ids_a), len(ids_b)))
    for i, ida in enumerate(ids_a):
        for j, idb in enumerate(ids_b):
            cost_matrix[i, j] = np.linalg.norm(features_a[ida] - features_b[idb])
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    mapping = {ids_b[j]: ids_a[i] for i, j in zip(row_ind, col_ind)}
    return mapping
