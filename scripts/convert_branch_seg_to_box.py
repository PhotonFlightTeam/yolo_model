from pathlib import Path

DATASET_ROOT = Path("datasets/raw/branch")
GLOBAL_BRANCH_CLASS = 5


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
invalid_objects = 0

for label_file in label_files:
    new_lines = []

    with open(label_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            try:
                coords = [float(value) for value in parts[1:]]
            except ValueError:
                print(f"Invalid numbers in: {label_file}")
                invalid_objects += 1
                continue

            if len(coords) < 6 or len(coords) % 2 != 0:
                print(f"Invalid polygon in: {label_file}")
                invalid_objects += 1
                continue

            x_center, y_center, width, height = polygon_to_box(coords)

            new_lines.append(
                f"{GLOBAL_BRANCH_CLASS} "
                f"{x_center:.6f} "
                f"{y_center:.6f} "
                f"{width:.6f} "
                f"{height:.6f}"
            )

            converted_objects += 1

    with open(label_file, "w", encoding="utf-8") as file:
        if new_lines:
            file.write("\n".join(new_lines) + "\n")


print("\n--- BRANCH CONVERSION COMPLETE ---")
print(f"Objects converted to global class 5: {converted_objects}")
print(f"Invalid objects skipped: {invalid_objects}")