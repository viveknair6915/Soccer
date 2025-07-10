import json
import os

def save_tracking_results(tracking_results, output_path):
    try:
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(tracking_results, f)
        print(f'[INFO] Tracking results saved to {output_path}')
    except Exception as e:
        print(f'[ERROR] Failed to save tracking results: {e}')
