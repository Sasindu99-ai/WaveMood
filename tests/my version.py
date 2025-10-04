import os
import numpy as np
import librosa
import joblib
from tensorflow.keras.models import load_model
from sklearn.neighbors import KNeighborsClassifier
import sounddevice as sd
from scipy.io.wavfile import write, read
import warnings
import serial
import time

warnings.filterwarnings("ignore")  # cleaner output

# ---------------- CONFIG ----------------
BASE_PATH = r"C:\Users\LENOVO\Desktop\mood"   # adjust to your folder
SR = 22050
FS = 44100

# Serial connection to Arduino (change COM3 if needed)
arduino = serial.Serial("COM6", 9600, timeout=1)
time.sleep(2)  # wait for Arduino to reset

# ---------------- LOAD MODELS ----------------
mlp_model = load_model(os.path.join(BASE_PATH, "emotiondetector_mlp_model.h5"))
scaler_mlp = joblib.load(os.path.join(BASE_PATH, "emotiondetectornlw_scaler.pkl"))
le_mlp = joblib.load(os.path.join(BASE_PATH, "emotiondetectornlw_labelencoder.pkl"))

knn_model = joblib.load(os.path.join(BASE_PATH, "knn_emotion_model.pkl"))
le_knn = joblib.load(os.path.join(BASE_PATH, "emotion_labelencoderknn.pkl"))

# ---------------- AUDIO FUNCTIONS ----------------
def record_audio(filename="output.wav", seconds=3):
    print(f"\n🎤 Recording for {seconds} seconds...")
    audio = sd.rec(int(seconds * FS), samplerate=FS, channels=1)
    sd.wait()
    write(filename, FS, audio)
    print(f"💾 Saved as {filename}")
    return filename

def play_audio(filename="output.wav"):
    fs, data = read(filename)
    print(f"\n🔊 Playing {filename}...")
    sd.play(data, fs)
    sd.wait()

# ---------------- FEATURE EXTRACTION ----------------
def load_fixed_duration(file_path, sr, duration=3.0):
    y, _ = librosa.load(file_path, sr=sr, duration=duration)
    target_length = int(sr * duration)
    y = librosa.util.fix_length(y, size=target_length)
    return y

def split_audio_pitch(file_path, sr):
    y = load_fixed_duration(file_path, sr, 3.0)
    Nw = int(sr * 0.6)
    f0 = librosa.yin(y, fmin=50, fmax=8000, sr=sr,
                     frame_length=Nw, hop_length=int(Nw/2), center=False)
    frames = librosa.util.frame(y, frame_length=Nw, hop_length=int(Nw/2))
    energy = np.sqrt(np.mean(frames**2, axis=0))
    return f0, energy

def ML_feed(f0, energy):
    f0 = np.nan_to_num(f0)
    energy = np.nan_to_num(energy)
    feed = [
        np.mean(f0), np.var(f0), np.max(f0), np.min(f0),
        np.mean(energy), np.var(energy), np.max(energy), np.min(energy)
    ]
    return np.array(feed).reshape(1, -1)

# ---------------- PREDICTION ----------------
def predict_emotion(model_type, features):
    if model_type == "mlp":
        scaled = scaler_mlp.transform(features)
        probs = mlp_model.predict(scaled, verbose=0)
        pred = np.argmax(probs, axis=1)
        emotion = le_mlp.inverse_transform(pred)[0]
    elif model_type == "knn":
        pred = knn_model.predict(features)
        emotion = le_knn.inverse_transform(pred)[0]
    else:
        raise ValueError("Unknown model type.")
    return emotion

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("🎤 Welcome to Emotion Detector")

    negative_emotions = {"angry", "fearful", "sad", "disgust"}
    positive_emotions = {"happy", "surprised", "calm", "excited"}

    while True:
        choice = input("\n👉 Do you want to start recording? (y/n): ").strip().lower()

        if choice == "y":
            filename = record_audio("output.wav", seconds=3)
            play_audio(filename)

            print("\nChoose model for prediction:")
            print("1 - MLP Neural Network")
            print("2 - KNN Classifier")
            model_choice = input("Enter 1 or 2: ").strip()

            if model_choice == "1":
                model_type = "mlp"
            elif model_choice == "2":
                model_type = "knn"
            else:
                print("❌ Invalid choice, skipping...")
                continue

            f0, energy = split_audio_pitch(filename, SR)
            features = ML_feed(f0, energy)
            emotion = predict_emotion(model_type, features)

            print(f"\n✅ Predicted Emotion: {emotion}")

            # Send to Arduino
            if emotion.lower() in negative_emotions:
                arduino.write(b"NEG\n")
                print("➡️ Sent NEG to Arduino (servo = 180°)")
            elif emotion.lower() in positive_emotions:
                arduino.write(b"POS\n")
                print("➡️ Sent POS to Arduino (servo = 180°)")
            else:
                print("⚠️ Emotion not mapped, nothing sent.")

        elif choice == "n":
            print("👋 Exiting program.")
            break
        else:
            print("❌ Please enter 'y' or 'n'.")
