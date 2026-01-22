"""
MODIFIED AUDIO MONITOR - Sends data to backend
Add this to your existing audio_monitor.py
"""
import sys
sys.path.insert(0, './backend')

from monitoring_client import get_monitoring_client

# Initialize monitoring client
monitoring_client = get_monitoring_client()
monitoring_client.start()

# After your existing code processes audio, add this:
# monitoring_client.send_audio_data(text, keywords=detected_keywords)

# Example integration in main loop:
# if detected_keywords:
#     monitoring_client.send_audio_data(
#         text=text,
#         keywords=detected_keywords,
#     )

# To use: Import this module before running audio_monitor.py
# Then uncomment the send_audio_data calls in your main loop
