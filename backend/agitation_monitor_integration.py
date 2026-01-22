"""
MODIFIED AGITATION MONITOR - Sends data to backend
Add this integration to your existing full_agitation_monitor.py
"""
import sys
sys.path.insert(0, './backend')

from monitoring_client import get_monitoring_client

# Initialize monitoring client
monitoring_client = get_monitoring_client()
monitoring_client.start()

# After your existing code calculates agitation, add this in the main loop:
# monitoring_client.send_agitation_data(
#     level=agitation_counter,
#     status=status_text,
#     head_speed=head_speed,
#     arm_speed=arm_speed,
# )

# Example location in full_agitation_monitor.py (around line 120):
# # ----- ADD THIS -----
# if frame_count % 5 == 0:  # Send every 5 frames to reduce overhead
#     monitoring_client.send_agitation_data(
#         level=agitation_counter,
#         status=status_text,
#         head_speed=head_speed,
#         arm_speed=arm_speed,
#     )
