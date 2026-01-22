import whisper
import sounddevice as sd
import numpy as np
import torch
import warnings
from datetime import datetime
from scipy import signal
import sys
warnings.filterwarnings('ignore')


sys.path.insert(0, './backend')
from monitoring_client import get_monitoring_client

monitoring_client = get_monitoring_client()
monitoring_client.start()
print("✓ Connected to dashboard backend")


# =========================================================================
# WHISPER + VOICE ACTIVITY DETECTION + NOISE REDUCTION
# =========================================================================

# Keywords to detect
KEYWORDS = ["help", "nurse", "pain", "doctor", "emergency", "breathe", "hurt", "ache"]

# Audio config
SAMPLERATE = 16000
DURATION = 5  # Seconds per recording chunk
DEVICE_ID = 2  # Microphone Array

# Voice Activity Detection thresholds
VAD_THRESHOLD = 0.05  # Minimum RMS level to consider speech
SPEECH_DURATION_MIN = 0.5  # Minimum speech duration in seconds
SILENCE_THRESHOLD = 0.02  # Background noise threshold

def detect_speech(audio, sr=16000):
    """
    Detect if audio contains meaningful speech using VAD.
    Returns True if speech is detected.
    """
    # Pre-emphasis filter to boost high frequencies (speech is higher frequency)
    pre_emphasis = 0.97
    audio_emphasized = np.append(audio[0], audio[1:] - pre_emphasis * audio[:-1])
    
    # Calculate RMS (Root Mean Square) energy
    frame_length = int(0.02 * sr)  # 20ms frames
    hop_length = int(0.01 * sr)    # 10ms hop
    
    frames = np.array([
        audio_emphasized[i:i + frame_length]
        for i in range(0, len(audio_emphasized) - frame_length, hop_length)
    ])
    
    # Calculate energy for each frame
    energies = np.sqrt(np.mean(frames**2, axis=1))
    
    # Dynamic threshold based on median energy
    median_energy = np.median(energies)
    speech_frames = energies > (median_energy * 2)  # Speech is >2x background
    
    # Need at least 0.5s of speech
    min_speech_frames = int(SPEECH_DURATION_MIN * sr / hop_length)
    speech_count = np.sum(speech_frames)
    
    return speech_count >= min_speech_frames

def reduce_noise(audio, sr=16000):
    """
    Simple noise reduction using spectral subtraction.
    """
    # Get noise profile from first 0.5s (assuming silence)
    noise_sample = audio[:int(0.5 * sr)]
    noise_spectrum = np.abs(np.fft.rfft(noise_sample))
    noise_mean = np.mean(noise_spectrum, axis=0)
    
    # Process full audio
    result = np.zeros_like(audio)
    frame_length = 512
    hop_length = frame_length // 2
    
    for i in range(0, len(audio) - frame_length, hop_length):
        frame = audio[i:i + frame_length]
        spectrum = np.abs(np.fft.rfft(frame))
        
        # Subtract noise, but keep floor to avoid over-suppression
        clean_spectrum = np.maximum(spectrum - noise_mean * 0.8, spectrum * 0.1)
        
        # Reconstruct phase
        phase = np.angle(np.fft.rfft(frame))
        clean_fft = clean_spectrum * np.exp(1j * phase)
        clean_frame = np.fft.irfft(clean_fft)
        
        # Overlap-add
        result[i:i + frame_length] += clean_frame * np.hanning(frame_length)
    
    # Normalize
    return result / (np.max(np.abs(result)) + 1e-8)

print("=" * 70)
print("WHISPER + VAD + NOISE REDUCTION AUDIO MONITOR")
print("=" * 70)

# Load Whisper model (tiny for speed, base for accuracy)
print("\n📥 Loading Whisper model (base)...")
model = whisper.load_model("base", device="cuda" if torch.cuda.is_available() else "cpu")
print("✓ Whisper model loaded!")

print("\n🎤 Audio Configuration:")
print(f"  Device ID: {DEVICE_ID} (Microphone Array)")
print(f"  Sample Rate: {SAMPLERATE} Hz")
print(f"  Recording Duration: {DURATION}s per chunk")
print(f"  Keywords: {KEYWORDS}")
print(f"  Speech Detection: VAD + Noise Reduction")
print(f"  Min Speech Duration: {SPEECH_DURATION_MIN}s")

print("\n" + "=" * 70)
print("Listening for distress keywords... Speak clearly!")
print("Press Ctrl+C to stop.")
print("=" * 70 + "\n")

chunk_count = 0

try:
    while True:
        chunk_count += 1
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Recording chunk #{chunk_count}...", end=" ", flush=True)
        
        try:
            # Record audio
            audio = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, 
                          channels=1, device=DEVICE_ID, dtype=np.float32)
            sd.wait()
            
            audio = audio.flatten()
            
            # Step 1: Check if there's actual speech (VAD)
            if not detect_speech(audio, SAMPLERATE):
                print("(silence - no speech detected)")
                continue
            
            # Step 2: Reduce noise
            print("\n  Denoising...", end=" ", flush=True)
            audio_clean = reduce_noise(audio, SAMPLERATE)
            
            # Step 3: Normalize
            audio_clean = audio_clean / (np.max(np.abs(audio_clean)) + 1e-8)
            
            print("Transcribing...", end=" ", flush=True)
            
            # Transcribe with Whisper
            result = model.transcribe(
                audio_clean,
                language="en",
                verbose=False,
                temperature=0.5,  # Greedy decoding
            )
            
            text = result["text"].strip().lower()
            
            if text and len(text) > 3:  # Only show results with meaningful text (>3 chars)
                print(f"✓\n  Heard: '{text}'")
                
                # Check for keywords
                detected_keywords = [kw for kw in KEYWORDS if kw in text]
                
                # Send to backend
                monitoring_client.send_audio_data(
                    text=text,
                    keywords=detected_keywords
                )
                
                if detected_keywords:
                    print("\n" + "!" * 70)
                    print(f"🚨 CRITICAL AUDIO ALERT: {detected_keywords} detected!")
                    print(f"   Transcription: '{text}'")
                    print(f"   Timestamp: {datetime.now().isoformat()}")
                    print("!" * 70)
                else:
                    print("   >> (No critical keywords detected)")
            else:
                print("(no meaningful speech)")
                
        except Exception as e:
            print(f"Error during transcription: {e}")
            continue

except KeyboardInterrupt:
    print("\n\n" + "=" * 70)
    print("Audio monitor stopped.")
    print("=" * 70)
