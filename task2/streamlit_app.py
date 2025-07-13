import streamlit as st
import cv2
import json
import numpy as np
import os
from pathlib import Path

st.set_page_config(page_title="Soccer Player Re-ID Dashboard (Task 2)", layout="wide")

st.title("⚽ Soccer Player Re-Identification Dashboard – Task 2: Single-Camera Re-ID")

DATA_DIR = Path("data/")
VIDEO_PATH = DATA_DIR / "output_broadcast_tracked.mp4"
TRACKING_JSON_PATH = DATA_DIR / "tracking_broadcast.json"

st.title("⚽ Soccer Player Re-Identification Dashboard")
st.markdown("""
This dashboard lets you:
- **Watch the tracked output video**
- **Explore player ID assignments frame-by-frame**
- **Visualize player trajectories and stats**
""")

# --- Upload and Process Video ---
st.header("1. Upload and Process Video")
import traceback
from pathlib import Path

def safe_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()

uploaded_file = st.file_uploader("Upload video to process", type=["mp4", "avi", "mov", "mkv"])
if uploaded_file:
    output_format = st.selectbox("Select output format", ["mp4", "avi"])
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
        output_base = Path(input_filename).stem
        output_path = data_dir / f"output_{output_base}_tracked.{output_format}"
        output_json = data_dir / f"tracking_{output_base}.json"
        try:
            with st.spinner("Processing video. This may take a while..."):
                from src.main import process_video
                process_video(str(input_path), str(model_path), str(output_path), str(output_json), label_filter='player', output_format=output_format)
            st.success(f"Processing complete! Output: {output_path.name}")
            st.video(str(output_path))
            with open(output_path, "rb") as out_f:
                st.download_button(f"Download Output ({output_format})", out_f, file_name=output_path.name)
        except Exception as e:
            st.error(f"Error during processing: {e}")
            st.code(traceback.format_exc())
    else:
        st.error(f"Model weights not found at {model_path} and could not be downloaded. Please upload best.pt to models/ directory or update the download URL.")

# --- Video Viewer ---
st.header("2. Tracked Output Video")
if VIDEO_PATH.exists():
    try:
        video_bytes = VIDEO_PATH.read_bytes()
        st.video(video_bytes)
    except Exception:
        st.error("Video could not be played in this browser. Try downloading it or using a different browser. If the file is corrupted, re-run the pipeline.")
    st.download_button(f"Download Output Video", VIDEO_PATH.read_bytes(), file_name=VIDEO_PATH.name)
else:
    st.warning(f"Video not found: {VIDEO_PATH}")

# --- Tracking Data Viewer ---
st.header("2. Tracking Data Explorer")
if TRACKING_JSON_PATH.exists():
    with open(TRACKING_JSON_PATH, "r") as f:
        tracking_data = json.load(f)
    st.write(f"Total frames: {len(tracking_data)}")
    frame_num = st.slider("Select frame:", 0, len(tracking_data)-1, 0)
    frame_info = tracking_data[frame_num]
    st.json(frame_info)
    # Player count per frame
    st.metric("Players in frame", len(frame_info['objects']))
else:
    st.warning(f"Tracking JSON not found: {TRACKING_JSON_PATH}")

# --- Player Statistics ---
st.header("3. Player Statistics")
if TRACKING_JSON_PATH.exists():
    player_counts = {}
    for frame in tracking_data:
        for pid in frame['objects'].keys():
            player_counts[pid] = player_counts.get(pid, 0) + 1
    if player_counts:
        st.subheader("Player Appearance Frequency (Bar Chart)")
        st.bar_chart(player_counts)
        st.markdown(f"**Total unique player IDs detected:** {len(player_counts)}")
        # Players per frame line chart
        st.subheader("Number of Players Detected Per Frame (Line Chart)")
        players_per_frame = [len(frame['objects']) for frame in tracking_data]
        st.line_chart(players_per_frame)
        # Trajectory plot
        st.subheader("Player Trajectories (Centroids)")
        import matplotlib.pyplot as plt
        player_traj = {}
        for frame in tracking_data:
            for pid, centroid in frame['objects'].items():
                if pid not in player_traj:
                    player_traj[pid] = []
                player_traj[pid].append(tuple(centroid))
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

st.markdown("---")
st.markdown("Developed by Vivek V Nair")
