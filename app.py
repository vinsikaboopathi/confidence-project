from flask import Flask, render_template, request
import librosa
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["audio"]

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    # LOAD AUDIO
    y, sr = librosa.load(filepath)

    # AUDIO ENERGY
    energy = np.mean(np.abs(y))

    # SCORE CALCULATION
    score = int(energy * 1000)

    if score > 100:
        score = 100

    if score < 30:
        score = 30

    # LEVEL
    if score >= 75:
        level = "HIGH"
        color = "#00ff99"

    elif score >= 50:
        level = "MEDIUM"
        color = "#ffaa00"

    else:
        level = "LOW"
        color = "#ff4444"

    return {
        "score": score,
        "level": level,
        "color": color
    }

if __name__ == "__main__":
    app.run(debug=True)