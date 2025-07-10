import os
import cv2
from detector import PlayerDetector
from tracker import PlayerTracker
from feature_extractor import extract_color_histogram
from player_mapper import load_tracking_json, extract_all_features, map_players
from utils import save_tracking_results
import json
from tqdm import tqdm

def process_video(video_path, model_path, output_video_path, output_json_path, label_filter='player'):
    detector = PlayerDetector(model_path)
    tracker = PlayerTracker(max_disappeared=15)
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
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
        for object_id, centroid in objects.items():
            cv2.circle(frame, tuple(centroid), 5, (0,255,0), -1)
            cv2.putText(frame, f'ID {object_id}', (centroid[0]-10, centroid[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        for bbox in player_boxes:
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)
        out.write(frame)
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

def main():
    model_path = os.path.join('models', 'best.pt')
    broadcast_path = os.path.join('data', 'broadcast.mp4')
    tacticam_path = os.path.join('data', 'tacticam.mp4')
    out_broadcast = os.path.join('data', 'output_broadcast_tracked.mp4')
    out_tacticam = os.path.join('data', 'output_tacticam_tracked.mp4')
    json_broadcast = os.path.join('data', 'tracking_broadcast.json')
    json_tacticam = os.path.join('data', 'tracking_tacticam.json')
    print('[STEP] Detecting and tracking players in broadcast video...')
    process_video(broadcast_path, model_path, out_broadcast, json_broadcast)
    print('[STEP] Detecting and tracking players in tacticam video...')
    process_video(tacticam_path, model_path, out_tacticam, json_tacticam)
    print('[STEP] Extracting appearance features and mapping IDs...')
    features_broadcast = extract_all_features(broadcast_path, load_tracking_json(json_broadcast))
    features_tacticam = extract_all_features(tacticam_path, load_tracking_json(json_tacticam))
    mapping = map_players(features_broadcast, features_tacticam)
    mapping_path = os.path.join('data', 'tacticam_to_broadcast_id_mapping.json')
    with open(mapping_path, 'w') as f:
        json.dump(mapping, f)
    print(f'[SUCCESS] Mapping saved to {mapping_path}')

if __name__ == "__main__":
    main()
