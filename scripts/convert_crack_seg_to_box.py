from pathlib import Path

DATASET_ROOT = Path("datasets/raw/crack")

# Local classes we want to keep and collapse into global crack class 1
KEEP_CLASSES = {0, 1, 2}

GLOBAL_CRACK_CLASS = 1


def polygon_to_box(coords):
    xs = coords[0::2]
    ys = coords[1::2]

    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2

    width = x_max - x_min
    height = y_max - y_min

    return x_center, y_center, width, height


label_files = [
    file
    for file in DATASET_ROOT.rglob("*.txt")
    if "labels" in [part.lower() for part in file.parts]
]

converted_objects = 0
skipped_objects = 0

for label_file in label_files:

    new_lines = []

    with open(label_file, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            try:
                class_id = int(parts[0])
                coords = [float(value) for value in parts[1:]]

            except ValueError:
                print(f"Skipping invalid line in {label_file}")
                continue

            # Ignore pothole, ravelling, rutting, striping
            if class_id not in KEEP_CLASSES:
                skipped_objects += 1
                continue

            # Already bounding-box format
            if len(parts) == 5:

                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])

            else:

                if len(coords) < 6 or len(coords) % 2 != 0:
                    print(f"Invalid polygon in {label_file}")
                    continue

                x_center, y_center, width, height = polygon_to_box(coords)

            new_lines.append(
                f"{GLOBAL_CRACK_CLASS} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{width:.6f} "
                f"{height:.6f}"
            )

            converted_objects += 1

    with open(label_file, "w", encoding="utf-8") as file:

        if new_lines:
            file.write("\n".join(new_lines) + "\n")


print("\n--- CONVERSION COMPLETE ---")
print(f"Converted crack objects: {converted_objects}")
print(f"Skipped non-crack objects: {skipped_objects}")