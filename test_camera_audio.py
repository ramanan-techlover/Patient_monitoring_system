"""
Quick test script to verify camera and audio devices are working
"""
import cv2
import sounddevice as sd
import sys

print("=" * 70)
print("DEVICE TEST UTILITY")
print("=" * 70)

# Test Camera
print("\n1. Testing Camera...")
cap = cv2.VideoCapture(0)
if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        print("   ✓ Camera is working!")
        print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")
        cv2.imshow("Camera Test - Press any key to close", frame)
        cv2.waitKey(2000)  # Show for 2 seconds
        cv2.destroyAllWindows()
    else:
        print("   ✗ Camera opened but couldn't read frame")
    cap.release()
else:
    print("   ✗ Could not open camera")
    print("   Make sure:")
    print("      - Camera is connected")
    print("      - No other app is using it")
    print("      - Camera permissions are granted")

# Test Microphone
print("\n2. Testing Microphone...")
try:
    devices = sd.query_devices()
    input_devices = [d for d in devices if d['max_input_channels'] > 0]
    
    if input_devices:
        print(f"   ✓ Found {len(input_devices)} microphone(s):")
        for i, device in enumerate(input_devices):
            if device['name'] == sd.query_devices(kind='input')['name']:
                print(f"      → {device['name']} (DEFAULT)")
            else:
                print(f"      - {device['name']}")
        
        # Test recording
        print("\n   Testing recording for 2 seconds...")
        recording = sd.rec(int(2 * 16000), samplerate=16000, channels=1)
        sd.wait()
        
        # Check if audio was captured
        if recording.max() > 0.01:
            print("   ✓ Microphone is working! (Detected audio)")
        else:
            print("   ⚠ Microphone opened but no audio detected")
            print("   Try speaking or check microphone volume")
    else:
        print("   ✗ No microphone devices found")
except Exception as e:
    print(f"   ✗ Error testing microphone: {e}")

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)

# Check if backend is running
print("\n3. Checking Backend Connection...")
try:
    import requests
    response = requests.get("http://localhost:5000/api/health", timeout=2)
    if response.status_code == 200:
        print("   ✓ Backend is running!")
    else:
        print(f"   ⚠ Backend responded with status {response.status_code}")
except:
    print("   ✗ Backend is not running")
    print("   Start it with: cd backend && python app.py")

print("\n✓ Ready to run monitoring scripts!")
