from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from detector import VehicleDetector
from traffic_logic import decide_signal_control

app = Flask(__name__)
detector = VehicleDetector()
LANES = ("north", "south", "east", "west")


def _parse_lane_counts(form_data: dict) -> dict[str, int]:
    lane_counts: dict[str, int] = {}
    for lane in LANES:
        raw_value = form_data.get(f"{lane}_count", "0")
        try:
            lane_counts[lane] = max(0, int(raw_value))
        except (TypeError, ValueError):
            lane_counts[lane] = 0
    return lane_counts


@app.route("/", methods=["GET"])
def dashboard():
    return render_template("index.html", lanes=LANES, result=None)


@app.route("/analyze", methods=["POST"])
def analyze():
    lane_counts = _parse_lane_counts(request.form)
    selected_emergency_lane = request.form.get("emergency_lane", "")
    emergency_lanes = [selected_emergency_lane] if selected_emergency_lane in LANES else []

    image_path = request.form.get("image_path", "").strip()
    image_lane = request.form.get("image_lane", "north")
    detection = None

    if image_path and image_lane in LANES:
        detection = detector.detect(image_path)
        detected_count = sum(detection["counts"].values())
        lane_counts[image_lane] += detected_count
        if detection["emergency_detected"] and image_lane not in emergency_lanes:
            emergency_lanes.append(image_lane)

    decision = decide_signal_control(lane_counts, emergency_lanes)
    result = {
        "lane_counts": lane_counts,
        "emergency_lanes": emergency_lanes,
        "decision": decision,
        "detection": detection,
    }

    return render_template("index.html", lanes=LANES, result=result)


@app.route("/api/analyze", methods=["POST"])
def analyze_api():
    payload = request.get_json(silent=True) or {}
    lane_counts = {lane: max(0, int(payload.get(lane, 0))) for lane in LANES}
    emergency_lanes = [lane for lane in payload.get("emergency_lanes", []) if lane in LANES]

    decision = decide_signal_control(lane_counts, emergency_lanes)
    return jsonify(
        {
            "lane": decision.lane,
            "green_duration": decision.green_duration,
            "reason": decision.reason,
            "lane_counts": lane_counts,
            "emergency_lanes": emergency_lanes,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
