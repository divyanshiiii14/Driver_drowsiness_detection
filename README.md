## Driver Drowsiness Detection System

A real-time driver drowsiness detection system that uses computer vision to identify eye closure and alert the driver to prevent accidents. Built using **Python**, **OpenCV**, and **Mediapipe/Dlib** for face landmark detection.

---

## 🚗 Project Overview

Driver fatigue is one of the major causes of road accidents.
This system monitors the driver’s eyes using a camera feed and detects signs of drowsiness using the **Eye Aspect Ratio (EAR)**.
If the eyes remain closed for a certain duration, the system triggers a loud alert.

---

## 🔍 Features

* Real-time eye tracking
* EAR (Eye Aspect Ratio) based drowsiness detection
* Alarm sound on sleepiness
* Works with:

  * Laptop webcam
  * Mobile camera (IP Webcam)
  * ESP32-CAM video feed
* Lightweight and fast
* Easy to run on any system

---

## 🧠 Tech Stack

* Python
* OpenCV
* Mediapipe (or Dlib for face landmarks)
* NumPy
* Playsound (for alarm)

---

## 📁 Project Structure

```
/driver-drowsiness-detection
│── main.py
│── alarm.mp3
│── shape_predictor.dat   (if using Dlib)
│── README.md
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install Dependencies

```
pip install opencv-python mediapipe numpy playsound
```

### 2️⃣ Run the Program

```
python main.py
```

---

## 📸 How It Works

1. Detects the driver's face
2. Extracts eye landmarks
3. Calculates eye aspect ratio (EAR)
4. If EAR < threshold → eyes closed
5. If closed for too long → alarm triggers

---

## 🛎️ Alert System

A loud alarm (MP3 file) plays to wake the driver when the system detects drowsiness for a continuous duration.

---

## 🖼️ Future Improvements

* Yawn detection
* Head pose detection
* Night vision mode
* Car dashboard integration
* IoT alert system with ESP32

---

## 🙌 Author

Divyanshi Chhabra
B.Tech Electronics Engineering
Driver Safety | Computer Vision | Embedded Systems

---

## ⭐ Show Your Support

If you like this project, give it a **⭐ star** on GitHub!
