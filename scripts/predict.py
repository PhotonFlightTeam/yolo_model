from ultralytics import YOLO
from collections import Counter
import sys
from pathlib import Path

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

MODEL_PATH = "models/trained/multi_anomaly_yolo_v1.pt"
CONFIDENCE_THRESHOLD = 0.01

# --------------------------------------------------
# GET IMAGE PATH FROM TERMINAL
# --------------------------------------------------

if len(sys.argv) < 2:
    print("Usage:")
    print(r"py -3.13 scripts\predict.py path\to\image.jpg")
    sys.exit(1)

IMAGE_PATH = sys.argv[1]

image_file = Path(IMAGE_PATH)

if not image_file.exists():
    print(f"ERROR: Image not found: {IMAGE_PATH}")
    sys.exit(1)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = YOLO(MODEL_PATH)

# --------------------------------------------------
# RUN PREDICTION
# --------------------------------------------------

results = model.predict(
    source=IMAGE_PATH,
    conf=CONFIDENCE_THRESHOLD,
    device=0,
    save=True
)

# --------------------------------------------------
# PRINT DETECTIONS
# --------------------------------------------------

print("\nDETECTIONS")
print("-" * 60)

found = False
counts = Counter()

for result in results:
    for box in result.boxes:

        found = True

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = model.names[class_id]

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        counts[class_name] += 1

        print(
            f"{class_name:<15} "
            f"{confidence * 100:6.2f}%   "
            f"box=({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})"
        )

# --------------------------------------------------
# NO DETECTIONS
# --------------------------------------------------

if not found:
    print("No objects detected.")

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

if found:
    print("\nSUMMARY")
    print("-" * 60)

    for class_name, count in counts.items():
        print(f"{class_name:<15} {count}")