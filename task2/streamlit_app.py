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

# --- Video Viewer ---
st.header("1. Tracked Output Video")
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
