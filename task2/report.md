# Task 2 Report: Single-Camera Player Re-Identification

**Developed by Vivek V Nair**

All methodology, results, and evaluation details are provided in the main `report.md` at the project root.

This folder only contains code outputs and scripts for Task 2.
 in Sports Footage

## Task: Single-Camera Player Re-Identification

### 1. Introduction
The objective is to track and re-identify soccer players within a single video, ensuring that players who leave and re-enter the frame are assigned consistent IDs. This simulates real-time analytics for sports events.
- **Visualization:** Annotate output video with bounding boxes and consistent player IDs.

## 3. Experiments & Results
- Tested on provided soccer video (`15sec_input_720p.mp4`). Consistent IDs maintained through occlusions and re-entries.
- Output includes tracked video (`output_broadcast_tracked.mp4`) and JSON (`tracking_broadcast.json`) with frame-by-frame ID assignments.

## 4. Challenges
- Handling long occlusions or players with similar appearance.
- Ensuring real-time speed and reproducibility.

## 5. Improvements
- Integrate deep appearance embeddings for more robust re-ID.
- Use advanced tracking (SORT/DeepSORT) for crowded scenes.

## 6. How to Run
See README.md for detailed instructions.

## 7. References
- Ultralytics YOLOv11 documentation
- OpenCV, numpy, scipy libraries
