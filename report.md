# Soccer Player Re-Identification Report

**Developed by Vivek V Nair**

## 1. Introduction
Player re-identification is a core challenge in sports analytics, especially when combining footage from multiple camera angles. This project addresses the problem by ensuring that each soccer player is assigned a consistent identity (ID) across both broadcast and tacticam video feeds. The solution leverages state-of-the-art detection, tracking, and appearance-based mapping techniques to achieve robust cross-camera ID consistency.

## 2. Approach & Methodology
### 2.1. Detection
- Used a fine-tuned YOLOv11 model (provided by the assignment) to detect all players and the ball in each frame of both videos.
- The model outputs bounding boxes and class labels for each detected object.

### 2.2. Tracking
- Implemented a centroid-based tracker to assign temporary IDs to each detected player within each video.

## 3. Modularity & Code Structure
- Each task is self-contained in its folder (`task1/`, `task2/`), with all scripts, requirements, and dashboards included.
- Modular pipeline: detection, tracking, feature extraction, mapping (Task 1), and utility scripts.
- Data, model weights, and outputs are kept outside the repo per `.gitignore` for clean submission.

## 4. Interactive Dashboards
- **Streamlit dashboards** for each task allow:
  - Video playback (with fallback/download if browser fails)
  - Frame-by-frame tracking data exploration
  - Player statistics (appearance frequency, trajectory plots)
  - Download of outputs (videos, JSONs)
  - User-friendly error handling

## 5. Experiments & Results
- **Task 1:**
  - Consistent IDs across both feeds for most frames
  - Robust mapping except during heavy occlusion or visually similar players
  - Outputs: tracked videos, mapping JSON, tracking JSONs
- **Task 2:**
  - Consistent IDs for players even after leaving/re-entering the frame
  - Minor ID switches during heavy occlusion or similar appearance
  - Input: `task2/data/15sec_input_720p.mp4`
  - Outputs: `output_broadcast_tracked.mp4`, `tracking_broadcast.json` in `task2/data/`
- **Dashboards**: Enable rapid validation and analytics for both tasks.

## 3. Experiments & Results
- **Detection & Tracking:** Successfully detected and tracked all visible players in both videos. Temporary IDs were assigned and visualized frame-by-frame.
- **Feature Extraction:** Extracted robust color histograms for each player, confirming unique and consistent features for all IDs.
- **Mapping:** Achieved one-to-one mapping of player IDs between tacticam and broadcast videos using the Hungarian algorithm, even in the presence of occlusions and re-entries.
- **Outputs:**
    - Tracked videos: `output_broadcast_tracked.mp4`, `output_tacticam_tracked.mp4`
    - Mapping JSON: `tacticam_to_broadcast_id_mapping.json`
    - Final mapped video: `output_tacticam_mapped.mp4`
- **Performance:** The pipeline runs efficiently on standard hardware, processing each video in under a few minutes.

## 4. Challenges & Solutions
- **Class Label Consistency:** Ensured the detection model’s output labels matched expected classes (e.g., 'player'), adjusting filters as needed.
- **Frame Alignment:** Carefully handled frame count mismatches between videos and tracking JSONs to avoid annotation errors.
- **Appearance Variability:** Used temporal aggregation of color features to mitigate lighting and occlusion effects.
- **Debugging Output:** Added robust debug prints and error handling to quickly identify and resolve issues during development.

## 5. Possible Improvements
- **Advanced Re-ID Features:** Integrate deep learning-based appearance embeddings or jersey number OCR for even more robust mapping.
- **Improved Tracking:** Replace the centroid tracker with a more advanced approach (e.g., SORT, DeepSORT) for better handling of crowded scenes.
- **Visualization:** Add confidence scores or mapping visualizations to highlight uncertain matches.
- **Real-Time Processing:** Optimize for lower latency to enable live analysis.

## 6. How To Run
- Please see the detailed instructions in `README.md`.
- All code, dependencies, and usage steps are provided for full reproducibility.

## 7. References
- Ultralytics YOLOv11 documentation
- OpenCV, numpy, scipy libraries
- [Hungarian Algorithm (scipy.optimize.linear_sum_assignment)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html)

---