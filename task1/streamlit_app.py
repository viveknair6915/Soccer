import streamlit as st
import cv2
import json
import numpy as np
import os
from pathlib import Path
import tempfile
import shutil
import subprocess

st.set_page_config(page_title="Soccer Player Re-ID Dashboard (Task 1)", layout="wide")

DATA_DIR = Path("data/")
VIDEO1_PATH = DATA_DIR / "output_broadcast_tracked.mp4"
VIDEO2_PATH = DATA_DIR / "output_tacticam_tracked.mp4"
MAPPED_VIDEO_PATH = DATA_DIR / "output_tacticam_mapped.mp4"
TRACKING1_JSON_PATH = DATA_DIR / "tracking_broadcast.json"
TRACKING2_JSON_PATH = DATA_DIR / "tracking_tacticam.json"
MAPPING_JSON_PATH = DATA_DIR / "tacticam_to_broadcast_id_mapping.json"

st.title("⚽ Soccer Player Re-Identification Dashboard – Task 1: Cross-Camera Mapping")
st.markdown("""
This dashboard lets you:
- **Watch all output videos**
- **Visualize tracking and mapping frame-by-frame with bounding boxes overlay**
- **Explore player ID assignments and mapping**
- **See player statistics and trajectory plots**
- **Download all outputs**
""")

# --- Video Selector ---
st.header("1. Output Videos")
video_options = {
    "Broadcast (Tracked)": VIDEO1_PATH,
    "Tacticam (Tracked)": VIDEO2_PATH,
    "Tacticam (Mapped IDs)": MAPPED_VIDEO_PATH,
}
video_choice = st.selectbox("Select video to view:", list(video_options.keys()))
video_path = video_options[video_choice]
if video_path.exists():
    try:
        st.video(video_path.read_bytes())
    except Exception:
        st.error("Video could not be played in this browser. Try downloading it or using a different browser. If the file is corrupted, re-run the pipeline.")
    st.download_button(f"Download {video_choice}", video_path.read_bytes(), file_name=video_path.name)
else:
    st.warning(f"Not found: {video_path}")

# --- Upload and Process Video ---
st.header("2. Upload and Process Video")
import traceback
from pathlib import Path

def safe_filename(name):
    # Remove potentially unsafe characters
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()

uploaded_file = st.file_uploader("Upload video to process", type=["mp4", "avi", "mov", "mkv"])
if uploaded_file:
    output_format = st.selectbox("Select output format", ["mp4", "avi"])
    # Save uploaded file
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    input_filename = safe_filename(uploaded_file.name)
    input_path = data_dir / input_filename
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Uploaded: {input_filename}")

    model_path = Path("models") / "best.pt"
    # --- Auto-download model weights if missing ---
    if not model_path.exists():
        st.info("Model weights not found. Attempting to download best.pt...")
        model_path.parent.mkdir(exist_ok=True)
        url = "https://drive.google.com/uc?export=download&id=11y3zZbqvwR76UiD2PtEPwpo0_wxt69J9"  # <-- Replace with your actual public link
        try:
            import requests
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(model_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            st.success("Model weights downloaded successfully.")
        except Exception as e:
            st.error(f"Failed to download model weights: {e}")
    if model_path.exists():
        import torch
        try:
            import ultralytics
        except ImportError:
            ultralytics = None
        st.info(f"Model path: {model_path.resolve()}\nSize: {model_path.stat().st_size} bytes\nTorch version: {torch.__version__}\nUltralytics version: {getattr(ultralytics, '__version__', 'not installed')}")
        output_base = Path(input_filename).stem
        output_path = data_dir / f"output_{output_base}_tracked.{output_format}"
        output_json = data_dir / f"tracking_{output_base}.json"
        try:
            with st.spinner("Processing video. This may take a while..."):
                from src.cross_camera_mapping import process_video
                process_video(str(input_path), str(model_path), str(output_path), str(output_json), label_filter='player', output_format=output_format)
            st.success(f"Processing complete! Output: {output_path.name}")
            st.video(str(output_path))
            with open(output_path, "rb") as out_f:
                st.download_button(f"Download Output ({output_format})", out_f, file_name=output_path.name)
        except Exception as e:
            st.error(f"Error during processing: {e}")
            st.code(traceback.format_exc())
            st.info("If you see a _pickle.UnpicklingError or 'invalid load key', please ensure your model was exported with the same Ultralytics and Torch version as shown above, and is a YOLOv8 PyTorch .pt file.")
    else:
        st.error(f"Model weights not found at {model_path} and could not be downloaded. Please upload best.pt to models/ directory or update the download URL.")

# --- Frame-by-frame Visualization ---
st.header("3. Frame-by-Frame Visualization")
json_options = {
    "Broadcast Tracking": TRACKING1_JSON_PATH,
    "Tacticam Tracking": TRACKING2_JSON_PATH,
}
json_choice = st.selectbox("Select tracking data:", list(json_options.keys()), key="json_choice")
json_path = json_options[json_choice]
if json_path.exists():
    with open(json_path, "r") as f:
        tracking_data = json.load(f)
    st.write(f"Total frames: {len(tracking_data)}")
    frame_num = st.slider("Select frame:", 0, len(tracking_data)-1, 0, key="frame_slider")
    frame_info = tracking_data[frame_num]
    st.json(frame_info)
    # Try to load and overlay bounding boxes on the video frame
    video_for_json = VIDEO1_PATH if json_choice == "Broadcast Tracking" else VIDEO2_PATH
    if video_for_json.exists():
        cap = cv2.VideoCapture(str(video_for_json))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if ret:
            # Draw bounding boxes
            for bbox, pid in zip(frame_info['boxes'], frame_info['objects'].keys()):
                x1, y1, x2, y2 = map(int, bbox)
                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f'ID {pid}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            # Show frame
            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption=f"Frame {frame_num}")
        cap.release()
else:
    st.warning(f"Not found: {json_path}")

# --- Mapping Viewer ---
st.header("3. Cross-Camera ID Mapping")
if MAPPING_JSON_PATH.exists():
    with open(MAPPING_JSON_PATH, "r") as f:
        mapping = json.load(f)
    st.write(f"Total mapped IDs: {len(mapping)}")
    st.json(mapping)
    st.download_button("Download Mapping JSON", json.dumps(mapping).encode(), file_name=MAPPING_JSON_PATH.name)
else:
    st.warning(f"Not found: {MAPPING_JSON_PATH}")

# --- Player Statistics & Trajectories ---
st.header("4. Player Statistics & Trajectories (Broadcast)")
if TRACKING1_JSON_PATH.exists():
    with open(TRACKING1_JSON_PATH, "r") as f:
        tracking1 = json.load(f)
    player_counts = {}
    player_traj = {}
    for frame in tracking1:
        for pid, centroid in frame['objects'].items():
            player_counts[pid] = player_counts.get(pid, 0) + 1
            if pid not in player_traj:
                player_traj[pid] = []
            player_traj[pid].append(tuple(centroid))
    if player_counts:
        st.subheader("Player Appearance Frequency (Bar Chart)")
        st.bar_chart(player_counts)
        st.markdown(f"**Total unique player IDs detected:** {len(player_counts)}")
        # Players per frame line chart
        st.subheader("Number of Players Detected Per Frame (Line Chart)")
        players_per_frame = [len(frame['objects']) for frame in tracking1]
        st.line_chart(players_per_frame)
        # Trajectory plot
        st.subheader("Player Trajectories (Centroids)")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        for pid, traj in player_traj.items():
            traj = np.array(traj)
            ax.plot(traj[:,0], traj[:,1], marker='o', label=f'ID {pid}')
        ax.set_title("Player Trajectories (Centroids)")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend(fontsize=7, loc='upper right', bbox_to_anchor=(1.18, 1))
        st.pyplot(fig)
    else:
        st.info("No player data available.")
else:
    st.info("No tracking data to analyze.")

# --- Download All Outputs ---
st.header("5. Download Outputs")
for file in [VIDEO1_PATH, VIDEO2_PATH, MAPPED_VIDEO_PATH, TRACKING1_JSON_PATH, TRACKING2_JSON_PATH, MAPPING_JSON_PATH]:
    if file.exists():
        st.download_button(f"Download {file.name}", file.read_bytes(), file_name=file.name)

st.markdown("---")
st.markdown("Developed by Vivek V Nair")
