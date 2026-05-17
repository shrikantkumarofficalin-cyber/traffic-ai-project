# traffic-ai-project

AI based traffic management and vehicle detection system using Python, YOLOv8, and Flask.

## Features

- YOLOv8-based vehicle detection integration (`ultralytics`)
- Emergency vehicle priority detection (model labels + filename keyword fallback)
- Adaptive traffic signal control based on congestion and emergency overrides
- Clean Flask web dashboard for manual lane inputs, optional image inference, and signal output
- JSON API endpoint for programmatic signal decisions
- Safe image-path handling (dashboard image paths are restricted to files inside the project directory)

## Project structure

- `/app.py` - Flask dashboard + API routes
- `/detector.py` - YOLOv8 detection wrapper
- `/traffic_logic.py` - Traffic signal decision logic
- `/templates/index.html` + `/static/style.css` - Dashboard UI
- `/tests/test_traffic_logic.py` - Focused logic tests

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open `http://127.0.0.1:5000`.

## API usage

`POST /api/analyze`

```json
{
  "north": 12,
  "south": 7,
  "east": 3,
  "west": 2,
  "emergency_lanes": ["south"]
}
```
