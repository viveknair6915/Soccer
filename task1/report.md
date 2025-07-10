# Task 1 Report: Cross-Camera Player Mapping

**Developed by Vivek V Nair**

All methodology, results, and evaluation details are provided in the main `report.md` at the project root.

This folder only contains code outputs and scripts for Task 1.


## 1. Introduction
This report details the approach and results for mapping# Player Re-Identification in Sports Footage

## Task: Cross-Camera Player Mapping
- **Re-Annotation:** Tacticam video is re-annotated with mapped (broadcast) IDs.

## 3. Experiments & Results
- Tracked and mapped all players across feeds.
- Outputs: `output_broadcast_tracked.mp4`, `output_tacticam_tracked.mp4`, `tacticam_to_broadcast_id_mapping.json`, `output_tacticam_mapped.mp4` in `task1/data/`.
- Pipeline is robust to occlusions and re-entries.

## 4. Challenges
- Ensuring label consistency, handling frame mismatches, robust feature matching.

## 5. Improvements
- Deep features, advanced trackers, mapping visualization.

## 6. How to Run
See README.md for instructions.

## 7. References
- Ultralytics YOLOv11 documentation
- OpenCV, numpy, scipy libraries
