from __future__ import annotations

from pathlib import Path

VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle"}
EMERGENCY_KEYWORDS = {"ambulance", "fire", "police", "emergency"}


class VehicleDetector:
    """YOLOv8 detector with graceful fallback when model/runtime is unavailable."""

    def __init__(self, model_name: str = "yolov8n.pt") -> None:
        self.model = None
        self.model_error = None

        try:
            from ultralytics import YOLO

            self.model = YOLO(model_name)
        except Exception as exc:  # pragma: no cover - depends on runtime availability
            self.model_error = str(exc)

    def detect(self, image_path: str, allowed_root: str | None = None) -> dict:
        counts = {"car": 0, "truck": 0, "bus": 0, "motorcycle": 0}
        emergency_detected = False
        labels: list[str] = []

        path = Path(image_path).expanduser().resolve()
        root = Path(allowed_root or Path.cwd()).expanduser().resolve()
        if root not in path.parents and path != root:
            return {
                "counts": counts,
                "emergency_detected": False,
                "labels": labels,
                "warning": f"Image path must be inside: {root}",
            }

        if not path.exists():
            return {
                "counts": counts,
                "emergency_detected": False,
                "labels": labels,
                "warning": f"Image not found: {image_path}",
            }

        if self.model is not None:
            try:
                result = self.model(str(path), verbose=False)[0]
                names = result.names
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    label = str(names[class_id]).lower()
                    labels.append(label)
                    if label in VEHICLE_CLASSES and label in counts:
                        counts[label] += 1
                    if any(keyword in label for keyword in EMERGENCY_KEYWORDS):
                        emergency_detected = True
            except Exception as exc:  # pragma: no cover - runtime/model specific
                return {
                    "counts": counts,
                    "emergency_detected": False,
                    "labels": labels,
                    "warning": f"YOLO inference failed: {exc}",
                }

        if any(keyword in path.name.lower() for keyword in EMERGENCY_KEYWORDS):
            emergency_detected = True

        return {
            "counts": counts,
            "emergency_detected": emergency_detected,
            "labels": labels,
            "warning": self.model_error,
        }
