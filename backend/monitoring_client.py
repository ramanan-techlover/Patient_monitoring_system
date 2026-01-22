"""
Integration module to send monitoring data to Flask backend
This should be imported by the monitoring scripts
"""
import requests
import json
from datetime import datetime
import threading
import queue

class MonitoringClient:
    """Client for sending monitoring data to Flask backend"""
    
    def __init__(self, server_url='http://localhost:5000'):
        self.server_url = server_url
        self.api_url = f"{server_url}/api"
        self.data_queue = queue.Queue()
        self.sender_thread = None
        self.running = False
        
    def start(self):
        """Start background thread for sending data"""
        if not self.running:
            self.running = True
            self.sender_thread = threading.Thread(target=self._send_loop, daemon=True)
            self.sender_thread.start()
    
    def stop(self):
        """Stop background thread"""
        self.running = False
    
    def _send_loop(self):
        """Background loop to send queued data"""
        while self.running:
            try:
                endpoint, data = self.data_queue.get(timeout=1)
                self._send_data(endpoint, data)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error sending data: {e}")
    
    def _send_data(self, endpoint, data):
        """Send data to backend"""
        try:
            url = f"{self.api_url}/{endpoint}"
            response = requests.post(url, json=data, timeout=5)
            if response.status_code == 200:
                print(f"✓ Data sent to {endpoint}")
            else:
                print(f"✗ Error sending to {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"✗ Connection error: {e}")
    
    # Pain Monitoring
    def send_pain_data(self, score, status, au04=None, au07=None, au10=None, async_send=False):
        """Send pain detection data"""
        data = {
            'score': score,
            'status': status,
            'au04': au04,
            'au07': au07,
            'au10': au10,
        }
        
        if async_send:
            self.data_queue.put(('pain/update', data))
        else:
            self._send_data('pain/update', data)
    
    # Agitation Monitoring
    def send_agitation_data(self, level, status, head_speed=None, arm_speed=None, async_send=False):
        """Send agitation detection data"""
        data = {
            'level': level,
            'status': status,
            'head_speed': head_speed,
            'arm_speed': arm_speed,
        }
        
        if async_send:
            self.data_queue.put(('agitation/update', data))
        else:
            self._send_data('agitation/update', data)
    
    # Audio Monitoring
    def send_audio_data(self, text, keywords=None, confidence=None, async_send=False):
        """Send audio transcription data"""
        data = {
            'text': text,
            'keywords': keywords or [],
            'confidence': confidence,
        }
        
        if async_send:
            self.data_queue.put(('audio/update', data))
        else:
            self._send_data('audio/update', data)
    
    def get_status(self, monitor_type):
        """Get current status from backend"""
        try:
            url = f"{self.api_url}/{monitor_type}/status"
            response = requests.get(url, timeout=5)
            return response.json()
        except Exception as e:
            print(f"Error getting status: {e}")
            return None
    
    def health_check(self):
        """Check if backend is running"""
        try:
            url = f"{self.api_url}/health"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False

# Global client instance
_client = None

def get_monitoring_client():
    """Get or create global monitoring client"""
    global _client
    if _client is None:
        _client = MonitoringClient()
    return _client

def send_pain_alert(score, status, au04=None, au07=None, au10=None):
    """Convenience function to send pain data"""
    client = get_monitoring_client()
    client.send_pain_data(score, status, au04, au07, au10)

def send_agitation_alert(level, status, head_speed=None, arm_speed=None):
    """Convenience function to send agitation data"""
    client = get_monitoring_client()
    client.send_agitation_data(level, status, head_speed, arm_speed)

def send_audio_alert(text, keywords=None, confidence=None):
    """Convenience function to send audio data"""
    client = get_monitoring_client()
    client.send_audio_data(text, keywords, confidence)
