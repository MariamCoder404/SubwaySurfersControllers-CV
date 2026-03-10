# 🎮 Subway Surfers — Gesture Controller

Control Subway Surfers (or any arrow-key game) using your **body** or **hand** — no keyboard needed. Two controller modes included.

---

## 🕹️ Two Controller Modes

| File | Mode | Uses |
|------|------|------|
| `body_controller.py` | Full body pose | Shoulders, arms, lean |
| `hand_controller.py` | One hand only | Fingers, wrist position |

---

## 📦 Requirements

- Python 3.8+
- Webcam

```bash
pip install opencv-python mediapipe pyautogui numpy
```

---

## ▶️ Run

```bash
# Body controller
python body_controller.py

# Hand controller
python hand_controller.py
```

> Make sure Subway Surfers (or your browser/emulator) is the **active window** before gesturing.

---

## 🧍 Body Controller — Gestures

| Action | Gesture |
|--------|---------|
| ⬆️ Jump | Raise **both arms** above shoulders |
| ⬇️ Roll | **Cross arms** on chest |
| ⬅️ Left lane | Lean body **left** |
| ➡️ Right lane | Lean body **right** |

**Tips:**
- Stand ~1.5–2m from your webcam so your full upper body is visible
- Press `R` to recalibrate if detection feels off
- Keep your background simple for better pose detection

---

## 🖐️ Hand Controller — Gestures

| Action | Gesture |
|--------|---------|
| ⬆️ Jump | Open hand — **5 fingers** |
| ⬇️ Roll | **Fist** — 0 fingers |
| ⬅️ Left lane | Move hand to **left** side of frame |
| ➡️ Right lane | Move hand to **right** side of frame |

**Tips:**
- Keep your hand clearly visible and well-lit
- The frame is divided into thirds: left (0–30%), center (30–70%), right (70–100%)

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Q` | Quit the controller |
| `R` | Recalibrate *(body controller only)* |


## 🐛 Troubleshooting

**No person / hand detected**
→ Improve lighting and make sure you're fully in frame

**Actions triggering too fast**
→ Increase the cooldown values in the `__init__` method

**Wrong window receiving keypresses**
→ Click on the game window first — PyAutoGUI sends to whatever is focused

**Pose not calibrating correctly**
→ Stand still in a neutral position for 1–2 seconds at startup, or press `R` to redo it

---
# ‼️Qick-start text file is so important, read it to start easily‼️
### Enjoy! 🤩💫
---

## 📄 License

MIT — free to use and modify.
