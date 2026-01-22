"""
MODIFIED PAIN MONITOR - Sends data to backend
Add this integration to your existing pain_monitor.py
"""
import sys
sys.path.insert(0, './backend')

from monitoring_client import get_monitoring_client

# Initialize monitoring client
monitoring_client = get_monitoring_client()
monitoring_client.start()

# After your existing code detects pain, add this:
# monitoring_client.send_pain_data(
#     score=current_pain_score,
#     status=status_text,
#     au04=au4,
#     au07=au7,
#     au10=au10,
# )

# Example location in pain_monitor.py (around line 70):
# # ----- ADD THIS -----
# if detected is not None and len(detected) > 0:
#     # Extract AU values
#     au4 = detected["AU04"].values[0]
#     au7 = detected["AU07"].values[0]
#     au10 = detected["AU10"].values[0]
#     current_pain_score = au4 + au7 + au10
#     
#     # SEND TO BACKEND
#     if frame_count % 10 == 0:  # Send every 10 frames to reduce overhead
#         monitoring_client.send_pain_data(
#             score=current_pain_score,
#             status=status_text,
#             au04=au4,
#             au07=au7,
#             au10=au10,
#         )
