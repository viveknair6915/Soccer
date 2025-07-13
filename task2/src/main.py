import cv2
import os
from src.detector import PlayerDetector
from src.tracker import PlayerTracker
from src.feature_extractor import extract_color_histogram
from src.utils import save_tracking_results
import numpy as np
from tqdm import tqdm

MODEL_PATH = os.path.join('models', 'best.pt')
VIDEO_PATH = os.path.join('data', '15sec_input_720p.mp4')
OUTPUT_VIDEO_PATH = os.path.join('data', 'output_broadcast_tracked.mp4')
OUTPUT_JSON_PATH = os.path.join('data', 'tracking_broadcast.json')

def process_video(video_path, model_path, output_video_path, output_json_path, label_filter='player', output_format='mp4'):
    detector = PlayerDetector(model_path)
    tracker = PlayerTracker(max_disappeared=15)
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*('mp4v' if output_format=='mp4' else 'XVID'))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    tracking_results = []
    frame_idx = 0
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), desc=f"Processing {os.path.basename(video_path)}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        detections = detector.detect(frame)
        player_boxes = [d['bbox'] for d in detections if d['label'].lower() == label_filter]
        objects = tracker.update(player_boxes)
        # Draw results
        for object_id, centroid in objects.items():
            cv2.circle(frame, tuple(centroid), 5, (0,255,0), -1)
            cv2.putText(frame, f'ID {object_id}', (centroid[0]-10, centroid[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        for bbox in player_boxes:
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
        out.write(frame)
        # Save tracking info
        tracking_results.append({
            'frame': frame_idx,
            'objects': {str(object_id): list(map(int, centroid)) for object_id, centroid in objects.items()},
            'boxes': [list(map(int, bbox)) for bbox in player_boxes]
        })
        frame_idx += 1
        pbar.update(1)
    pbar.close()
    cap.release()
    out.release()
    save_tracking_results(tracking_results, output_json_path)
    print(f'[SUCCESS] Output video saved to {output_video_path}')

if __name__ == "__main__":
    process_video(VIDEO_PATH, MODEL_PATH, OUTPUT_VIDEO_PATH, OUTPUT_JSON_PATH, label_filter='player', output_format='mp4')
