import cv2
import mediapipe as mp
import math
import time
import sys

# Backend Integration
sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

monitoring_client = get_monitoring_client()
monitoring_client.start()
print("✓ Connected to dashboard backend")

# ---------------------------------------------------------
# 1. SETUP & CONFIGURATION
# ---------------------------------------------------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Use '0' for Webcam, or put 'path/to/video.mp4' to test with a file
cap = cv2.VideoCapture(0)

# --- SENSITIVITY SETTINGS (Tweak these!) ---
# How much movement is considered "Fast"? (0.02 = 2% of screen distance)
HEAD_THRESH = 0.02
ARM_THRESH  = 0.035 

# Alert Logic
AGITATION_LIMIT = 20    # How many "bad frames" before Red Alert
COOLDOWN_RATE = 1       # How fast the meter drops when still
agitation_counter = 0

# State Variables
prev_landmarks = {} # Stores x,y for nose, wrists
prev_time = time.time()

print("Full-Body Agitation Monitor Active. Press 'q' to quit.")

# ---------------------------------------------------------
# 2. HELPER FUNCTION
# ---------------------------------------------------------
def calculate_movement(curr, prev):
    """Returns Euclidean distance between two (x,y) points"""
    if prev is None: return 0.0
    return math.sqrt((curr[0] - prev[0])**2 + (curr[1] - prev[1])**2)

# ---------------------------------------------------------
# 3. MAIN LOOP
# ---------------------------------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or camera error.")
        break

    # MediaPipe needs RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    status_text = "Calm"
    status_color = (0, 255, 0) # Green
    
    # Debug values to show on screen
    head_speed = 0.0
    arm_speed = 0.0

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        
        # -------------------------------------------------
        # A. GET COORDINATES (Nose + Wrists)
        # -------------------------------------------------
        # Indices: Nose=0, Left Wrist=15, Right Wrist=16
        curr_nose  = (lm[0].x, lm[0].y)
        curr_lwrist = (lm[15].x, lm[15].y)
        curr_rwrist = (lm[16].x, lm[16].y)

        # -------------------------------------------------
        # B. CALCULATE SPEEDS
        # -------------------------------------------------
        # Retrieve previous positions (if they exist)
        prev_nose = prev_landmarks.get('nose')
        prev_lwrist = prev_landmarks.get('lwrist')
        prev_rwrist = prev_landmarks.get('rwrist')

        if prev_nose and prev_lwrist and prev_rwrist:
            # 1. Head Movement
            head_speed = calculate_movement(curr_nose, prev_nose)
            
            # 2. Arm Movement (Max of left or right arm)
            l_speed = calculate_movement(curr_lwrist, prev_lwrist)
            r_speed = calculate_movement(curr_rwrist, prev_rwrist)
            arm_speed = max(l_speed, r_speed)

            # ---------------------------------------------
            # C. DECISION LOGIC (The "Brain")
            # ---------------------------------------------
            is_moving_head = head_speed > HEAD_THRESH
            is_moving_arms = arm_speed > ARM_THRESH
            
            # Weighted Logic: Arm movement is more dangerous (counts double)
            if is_moving_arms:
                agitation_counter += 2
                cv2.putText(frame, "ARM MOVEMENT!", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            elif is_moving_head:
                agitation_counter += 1
                cv2.putText(frame, "Head Toss", (50, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,165,255), 2)
            else:
                # Cool down if still
                if agitation_counter > 0:
                    agitation_counter -= COOLDOWN_RATE

            # Clamp counter
            agitation_counter = max(0, min(agitation_counter, AGITATION_LIMIT + 10))
            
            # Send to Dashboard Backend (every 5 frames)
            if results.pose_landmarks:
                monitoring_client.send_agitation_data(
                    level=int(agitation_counter),
                    status="CRITICAL" if agitation_counter >= AGITATION_LIMIT else "WARNING" if agitation_counter > AGITATION_LIMIT/2 else "CALM",
                    head_speed=float(head_speed),
                    arm_speed=float(arm_speed)
                )

        # Update History
        prev_landmarks['nose'] = curr_nose
        prev_landmarks['lwrist'] = curr_lwrist
        prev_landmarks['rwrist'] = curr_rwrist

        # Draw Skeleton
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # -----------------------------------------------------
    # 4. ALERTS & UI
    # -----------------------------------------------------
    if agitation_counter >= AGITATION_LIMIT:
        status_text = "CRITICAL: PATIENT THRASHING"
        status_color = (0, 0, 255) # Red
    elif agitation_counter > (AGITATION_LIMIT / 2):
        status_text = "Warning: Restless"
        status_color = (0, 255, 255) # Yellow

    # Draw Status Bar
    cv2.rectangle(frame, (0, 0), (640, 60), status_color, -1)
    
    # Text
    info = f"{status_text} | Level: {agitation_counter}"
    cv2.putText(frame, info, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
    
    # Debug Stats (Bottom Left)
    stats = f"Head Spd: {head_speed:.3f} | Arm Spd: {arm_speed:.3f}"
    cv2.putText(frame, stats, (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

    cv2.imshow('ICU Full Body Watcher', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()