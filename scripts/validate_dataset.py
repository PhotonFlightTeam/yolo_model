from pathlib import Path
import sys

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def find_images(folder):
    return [
        file
        for file in folder.rglob("*")
        if file.suffix.lower() in IMAGE_EXTENSIONS
    ]


def find_labels(folder):
    return [
        file
        for file in folder.rglob("*.txt")
        if "labels" in [part.lower() for part in file.parts]
    ]


def validate_dataset(dataset_name):
    dataset_root = Path("datasets/raw") / dataset_name

    if not dataset_root.exists():
        print(f"\nERROR: Dataset does not exist:")
        print(dataset_root)
        return

    images = find_images(dataset_root)
    labels = find_labels(dataset_root)

    print("\n================================")
    print(f" DATASET: {dataset_name}")
    print("================================")

    print(f"Images found:      {len(images)}")
    print(f"Label files found: {len(labels)}")

    invalid_labels = 0
    class_counts = {}

    for label_file in labels:

        with open(label_file, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                # YOLO detection labels should contain:
                # class_id x_center y_center width height

                if len(parts) != 5:
                    print(
                        f"INVALID FORMAT: {label_file} "
                        f"line {line_number}: {line}"
                    )
                    invalid_labels += 1
                    continue

                try:
                    class_id = int(parts[0])

                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])

                except ValueError:

                    print(
                        f"INVALID NUMBER: {label_file} "
                        f"line {line_number}: {line}"
                    )

                    invalid_labels += 1
                    continue

                coordinates = [
                    x_center,
                    y_center,
                    width,
                    height
                ]

                if not all(0 <= value <= 1 for value in coordinates):

                    print(
                        f"OUT OF RANGE: {label_file} "
                        f"line {line_number}: {line}"
                    )

                    invalid_labels += 1

                class_counts[class_id] = (
                    class_counts.get(class_id, 0) + 1
                )

    print("\n--- CLASS COUNTS ---")

    if not class_counts:
        print("No labeled objects found.")

    else:
        for class_id, count in sorted(class_counts.items()):
            print(f"Class {class_id}: {count} objects")

    print("\n--- RESULTS ---")

    if invalid_labels == 0:
        print("All checked YOLO labels appear valid.")
    else:
        print(f"Invalid labels found: {invalid_labels}")

    print()


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("\nUsage:")
        print(
            "py -3.13 scripts\\validate_dataset.py <dataset_name>"
        )

        print("\nExamples:")
        print(
            "py -3.13 scripts\\validate_dataset.py pothole"
        )
        print(
            "py -3.13 scripts\\validate_dataset.py crack"
        )

        sys.exit(1)

    dataset_name = sys.argv[1]

    validate_dataset(dataset_name)