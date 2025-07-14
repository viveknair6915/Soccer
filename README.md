# Soccer Player Re-Identification Assignment

**Developed by Vivek V Nair**

**Company:** Liat.ai  
**Role:** AI Intern  
**Assignment:** Player Re-Identification in Sports Footage

---

## 🚀 Live Dashboards

<table>
<tr>
<td>
<b>Task 1: Cross-Camera Mapping</b><br>
<a href="https://soccer-8yec.onrender.com/"><img src="./task1/Screenshots/Screenshot 2025-07-14 130447.png" width="400"/></a><br>
<a href="https://soccer-8yec.onrender.com/">Live Demo</a>
</td>
<td>
<b>Task 2: Single-Camera Re-ID</b><br>
<a href="https://soccer-task-2.onrender.com/"><img src="./task2/Screenshots/Screenshot 2025-07-14 141102.png" width="400"/></a><br>
<a href="https://soccer-task-2.onrender.com/">Live Demo</a>
</td>
</tr>
</table>

## Overview
This project solves the real-world challenge of player re-identification in soccer videos, ensuring that each player retains the same ID even across different camera feeds or after leaving and re-entering the frame. The solution is organized into two modular tasks:
- **Task 1:** Cross-Camera Player Mapping
- **Task 2:** Single-Camera Player Re-Identification

All code, documentation, and dashboards are self-contained in each task folder for easy evaluation.

---

## Evaluation Criteria
- **Accuracy and reliability** of player re-identification
- **Simplicity, modularity, and clarity** of code
- **Documentation quality** (README, report, code comments)
- **Runtime efficiency and latency** (bonus)
- **Creativity and thoughtfulness** of the approach

---

## Project Structure
```
Soccer/
├── README.md        # This file (project-level overview)
├── report.md        # Detailed project report (for download/submission)
├── task1/           # Task 1: Cross-Camera Player Mapping
│   ├── README.md
│   ├── report.md
│   ├── requirements.txt
│   ├── streamlit_app.py
│   └── src/
│       ├── cross_camera_mapping.py
│       ├── detector.py
│       ├── tracker.py
│       ├── feature_extractor.py
│       ├── player_mapper.py
│       └── utils.py
├── task2/           # Task 2: Single-Camera Player Re-Identification
│   ├── README.md
│   ├── report.md
│   ├── requirements.txt
│   ├── streamlit_app.py
│   └── src/
│       ├── main.py
│       ├── detector.py
│       ├── tracker.py
│       ├── feature_extractor.py
│       └── utils.py
```

---

## Setup Instructions
1. **Clone or download** this repository.
2. **Download the YOLOv11 model weights** (`best.pt`) from the assignment link and place them in the appropriate folder if needed.
3. **Download the input videos** from the assignment link and place them as described in each task's README.
4. **Install dependencies** for each task separately:
   ```bash
   cd task1
   pip install -r requirements.txt
   cd ../task2
   pip install -r requirements.txt
   ```

---

## Usage
### Task 1: Cross-Camera Player Mapping
- [Live Demo](https://soccer-8yec.onrender.com/)
- See [task1/README.md](./task1/README.md) for details and screenshot.
- Run the main pipeline:
  ```bash
  python src/cross_camera_mapping.py
  ```
- Launch the dashboard:
  ```bash
  streamlit run streamlit_app.py
  ```

### Task 2: Single-Camera Player Re-Identification
- See `task2/README.md` for full instructions.
- Place your input video as `task2/data/15sec_input_720p.mp4`.
- Run the main pipeline:
  ```bash
  python src/main.py
  ```
- Launch the dashboard:
  ```bash
  streamlit run streamlit_app.py
  ```
- Outputs will be generated as `output_broadcast_tracked.mp4` and `tracking_broadcast.json` in `task2/data/`.

---

## Troubleshooting
- If videos do not play in-browser, download and play locally or try a different browser.
- Ensure all files are in the correct folders as described in each task's README.
- For codec issues, re-encode videos using ffmpeg (see report for details).

---

## Contact
**Developed by Vivek V Nair**  

## Introduction
This project solves the real-world challenge of player re-identification in sports analytics. Given two synchronized soccer game videos from different camera angles (broadcast and tacticam), our pipeline ensures that each player is assigned a consistent ID across both feeds—even as they move, leave, or re-enter the frame. This is crucial for downstream analytics, tactical reviews, and automated highlight generation.

## Key Features
- **Robust Player Detection:** Uses a fine-tuned YOLOv11 model for accurate detection of players and the ball.
- **Tracking:** Assigns unique IDs to each player within both videos using a centroid-based tracker.
- **Appearance-Based Mapping:** Extracts color histogram features for each player and uses the Hungarian algorithm to match identities between the two camera views.
- **Output Generation:** Produces annotated videos and JSONs with consistent player IDs across both feeds.
- **Modular & Extensible:** Clean code structure for easy experimentation and future improvements.

## Directory Structure
```
Soccer/
├── src/                         # Source code (detection, tracking, mapping, utils)
├── models/                      # Model weights (see below)
├── data/                        # Input videos, outputs, and JSONs
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── report.md                    # Project report
```

## Setup & Usage
### 1. Download Required Files
- **YOLOv11 Model Weights:** [Google Drive Link](https://drive.google.com/file/d/1-5fOSHO_SB9UXYP_enOoZNAM_ScrePVCMD/view)
  - Place as `models/best.pt`
- **Videos:** [Assignment Folder](https://drive.google.com/drive/folders/1Nx6H_n0UUI6L-6i8WknXd4Cv2c3VjZTP?usp=sharing)
  - Place `broadcast.mp4` and `tacticam.mp4` in `task1/data/`
- Place `15sec_input_720p.mp4` in `task2/data/`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Pipeline
```bash
python src/cross_camera_mapping.py
```
This will:
- Detect and track players in both videos
- Extract appearance features and map IDs across feeds
- Generate all outputs in the `data/` folder

## Output Files (in `data/`)
| File                                 | Description                                      |
|--------------------------------------|--------------------------------------------------|
| output_broadcast_tracked.mp4         | Broadcast video with tracked player IDs           |
| output_tacticam_tracked.mp4          | Tacticam video with tracked player IDs            |
| tracking_broadcast.json              | Frame-by-frame tracking data for broadcast        |
| tracking_tacticam.json               | Frame-by-frame tracking data for tacticam         |
| tacticam_to_broadcast_id_mapping.json| Mapping of tacticam IDs to broadcast IDs          |
| output_tacticam_mapped.mp4           | Tacticam video with mapped (broadcast) IDs        |

## Evaluation Criteria & How We Addressed Them
- **Accuracy & Reliability:**
  - Uses appearance features (color histograms) and optimal assignment for robust mapping.
  - Handles occlusions and re-entries by leveraging tracking and feature aggregation.
- **Simplicity & Modularity:**
  - Code is split into logical modules: detection, tracking, feature extraction, mapping, annotation.
  - Easy to extend with new tracking or re-ID methods.
- **Documentation:**
  - This README and `report.md` explain every step.
  - Each script and function is commented for clarity.
- **Runtime Efficiency:**
  - Efficient OpenCV and numpy operations; batch processing where possible.
- **Thoughtfulness & Creativity:**
  - Explains methodology, challenges, and possible improvements in the report.
  - Extensible for more advanced re-ID features (deep learning, jersey OCR, etc.).

## Troubleshooting & Tips
- **Output video is empty/small:** Check that your input videos and model weights are correctly placed and not corrupted.
- **No players detected:** Ensure the model path is correct and matches the assignment's YOLOv11 weights.
- **Dependency errors:** Run `pip install -r requirements.txt` and ensure Python 3.8+ is used.
- **Custom improvements:** Try extending `src/tracker.py` or `src/feature_extractor.py` for more robust tracking or feature extraction.