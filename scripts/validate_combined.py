from pathlib import Path

DATASET_ROOT = Path("datasets/combined")

VALID_CLASSES = {
    0: "pothole",
    1: "crack",
    2: "trash",
    3: "rock",
    4: "tree",
    5: "branch",
    6: "light_pole",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

class_counts = {}
invalid_labels = 0

print("\n================================")
print(" COMBINED DATASET VALIDATION")
print("================================")

for split in ["train", "val", "test"]:

    image_dir = DATASET_ROOT / "images" / split
    label_dir = DATASET_ROOT / "labels" / split

    images = [
        f for f in image_dir.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS
    ]

    labels = list(label_dir.glob("*.txt"))

    print(f"\n{split.upper()}")
    print(f"Images: {len(images)}")
    print(f"Labels: {len(labels)}")

    for label_file in labels:

        with open(label_file, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) != 5:
                    print(
                        f"INVALID FORMAT: {label_file} "
                        f"line {line_number}"
                    )
                    invalid_labels += 1
                    continue

                try:
                    class_id = int(parts[0])

                    x = float(parts[1])
                    y = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])

                except ValueError:

                    print(
                        f"INVALID NUMBER: {label_file} "
                        f"line {line_number}"
                    )

                    invalid_labels += 1
                    continue

                if class_id not in VALID_CLASSES:

                    print(
                        f"INVALID CLASS {class_id}: "
                        f"{label_file}"
                    )

                    invalid_labels += 1
                    continue

                if not all(0 <= value <= 1 for value in [x, y, w, h]):

                    print(
                        f"OUT OF RANGE: {label_file} "
                        f"line {line_number}"
                    )

                    invalid_labels += 1

                class_counts[class_id] = (
                    class_counts.get(class_id, 0) + 1
                )


print("\n================================")
print(" GLOBAL CLASS COUNTS")
print("================================")

for class_id in sorted(VALID_CLASSES):

    count = class_counts.get(class_id, 0)

    print(
        f"{class_id} "
        f"{VALID_CLASSES[class_id]:12} "
        f"{count} objects"
    )


print("\n================================")
print(" RESULTS")
print("================================")

if invalid_labels == 0:
    print("All combined YOLO labels appear valid.")
else:
    print(f"Invalid labels found: {invalid_labels}")