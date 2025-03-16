# 🛳️ ShipMap - Live Research Vessel Tracker

This is a simple Flask + Leaflet web app to visualize live ship track data from the WHOI intranet server. It fetches the latest `.xy` file from the Atlantis map service, parses it, and displays:

- 🚢 Live-updating ship track (auto-refreshes every 5 min)
- 🟢 Current ship position marker
- 🌊 Optional bathymetry overlay (GEBCO 2023 WMS)
- 🌒 Day/night terminator overlay
- 🧭 Fully self-contained — runs locally with Python

---

## 🔧 Setup Instructions (Windows)

> See [`README-windows.txt`](README-windows.txt) for quick-start instructions for lab users.

### 1. Install Python
Download from [python.org](https://www.python.org/downloads/windows/) and ensure ✅ "Add Python to PATH" is checked.

### 2. Install Dependencies

Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
```

### 3. Run the App

On Windows, just double-click `run_shipmap.bat`

Or, from terminal:

```bash
python app.py
```

Then browse to:

```
http://localhost:5000/
```

### Folder structure:
```
shipmap/
├── app.py                 # Flask server
├── requirements.txt       # Python dependencies
├── run_shipmap.bat        # Windows launcher script
├── README.md              # This file
├── README-windows.txt     # For lab users
├── templates/
│   └── index.html         # Leaflet map page
```

### Example:
![Screenshot](screenshot.jpg)

