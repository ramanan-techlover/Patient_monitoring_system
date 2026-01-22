import cv2
from feat import Detector
import pandas as pd
import warnings
import traceback
import os
import sys
warnings.filterwarnings('ignore')  # Suppress FutureWarnings

# Backend Integration
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

monitoring_client = get_monitoring_client()
monitoring_client.start()
print("✓ Connected to dashboard backend")

# 1. Initialize the AI "Watcher" (Downloads models on first run)
# We use 'svm' for speed. If you have a strong GPU, use 'xgb'.
print("Loading AI Models... (this may take a moment)")
try:
    detector = Detector(
        au_model = "svm",      # Fast Action Unit detector
        emotion_model = "resmasknet", 
        face_model = "retinaface",
        device = "cuda"        # Use GPU acceleration
    )
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    traceback.print_exc()
    exit(1)

# 2. Setup Webcam (0 is usually the default laptop cam)
cap = cv2.VideoCapture(0)

# Constants
PAIN_THRESHOLD = 1.5   # Adjust sensitivity (0.0 to 5.0)
SKIP_FRAMES = 30       # Process 1 out of every 30 frames for speed (was 5)

frame_count = 0
current_pain_score = 0
status_color = (0, 255, 0) # Green (Safe)
status_text = "COMFORT"
temp_img_path = "temp_frame.jpg"  # Temporary file for py-feat

print("Watcher Active. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    
    # 3. AI Processing (Only runs every N frames to keep video smooth)
    if frame_count % SKIP_FRAMES == 0:
        try:
            print(f"Processing frame {frame_count}...")
            # Save current frame temporarily
            cv2.imwrite(temp_img_path, frame)
            
            # Detect faces and action units - pass file path
            detected = detector.detect_image(temp_img_path, output_size=320)
            
            print(f"Detection complete. Result: {type(detected)}, Rows: {len(detected) if detected is not None else 0}")
            
            if detected is not None and len(detected) > 0:
                # Extract the specific "Grimace" muscles
                # Note: Py-Feat returns a DataFrame, we take the first face found
                au4  = detected["AU04"].values[0] # Brow Lowerer
                au7  = detected["AU07"].values[0] # Lid Tightener
                au10 = detected["AU10"].values[0] # Upper Lip Raiser
                
                print(f"AU Values - AU04: {au4:.3f}, AU07: {au7:.3f}, AU10: {au10:.3f}")
                
                # Calculate Pain Score
                # Some models return 0-1, others 0-5. We sum them up.
                current_pain_score = au4 + au7 + au10
                
                # Send to Dashboard Backend (every 10 frames)
                if frame_count % 10 == 0:
                    monitoring_client.send_pain_data(
                        score=float(current_pain_score),
                        status="PAIN DETECTED" if current_pain_score > PAIN_THRESHOLD else "COMFORT",
                        au04=float(au4),
                        au07=float(au7),
                        au10=float(au10)
                    )
                
                # Decision Logic
                if current_pain_score > PAIN_THRESHOLD:
                    status_text = f"PAIN DETECTED (Score: {current_pain_score:.2f})"
                    status_color = (0, 0, 255) # Red (Danger)
                    print(f"⚠️ PAIN DETECTED! Score: {current_pain_score:.2f}")
                else:
                    status_text = f"Comfortable (Score: {current_pain_score:.2f})"
                    status_color = (0, 255, 0) # Green (Safe)
                    print(f"✓ Comfortable. Score: {current_pain_score:.2f}")
            else:
                status_text = "No Face Detected"
                status_color = (255, 0, 0) # Blue
                print("No face detected in frame")
                
        except KeyboardInterrupt:
            print("\nStopping...")
            break
        except Exception as e:
            print(f"Error during detection: {e}")
            traceback.print_exc()
            status_text = "Error - Check Console"
            status_color = (200, 200, 0) # Yellow

    # 4. Visual Feedback (Draw on the video)
    # Draw a bar at the top
    cv2.rectangle(frame, (0, 0), (640, 50), status_color, -1)
    cv2.putText(frame, status_text, (20, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Show the video
    cv2.imshow('ICU Pain Watcher', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Clean up temp file
if os.path.exists(temp_img_path):
    os.remove(temp_img_path)