from pathlib import Path
import shutil

RAW_ROOT = Path("datasets/raw")
COMBINED_ROOT = Path("datasets/combined")

DATASETS = [
    "pothole",
    "crack",
    "trash",
    "rock",
    "tree",
    "branch",
    "light_pole",
]

SPLIT_MAP = {
    "train": "train",
    "valid": "val",
    "val": "val",
    "test": "test",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def reset_combined():
    if COMBINED_ROOT.exists():
        shutil.rmtree(COMBINED_ROOT)

    for split in ["train", "val", "test"]:
        (COMBINED_ROOT / "images" / split).mkdir(parents=True, exist_ok=True)
        (COMBINED_ROOT / "labels" / split).mkdir(parents=True, exist_ok=True)


def copy_dataset(dataset_name):
    dataset_root = RAW_ROOT / dataset_name

    print(f"\nProcessing: {dataset_name}")

    copied_images = 0
    copied_labels = 0

    for source_split, target_split in SPLIT_MAP.items():
        image_dir = dataset_root / source_split / "images"
        label_dir = dataset_root / source_split / "labels"

        if not image_dir.exists():
            continue

        images = [
            image
            for image in image_dir.iterdir()
            if image.suffix.lower() in IMAGE_EXTENSIONS
        ]

        for index, image_path in enumerate(images):

            # Short unique filename
            new_stem = f"{dataset_name}_{source_split}_{index:06d}"

            new_image_name = new_stem + image_path.suffix.lower()

            target_image_path = (
                COMBINED_ROOT
                / "images"
                / target_split
                / new_image_name
            )

            shutil.copy2(image_path, target_image_path)
            copied_images += 1

            # Original matching YOLO label
            label_path = label_dir / f"{image_path.stem}.txt"

            if label_path.exists():
                target_label_path = (
                    COMBINED_ROOT
                    / "labels"
                    / target_split
                    / f"{new_stem}.txt"
                )

                shutil.copy2(label_path, target_label_path)
                copied_labels += 1

    print(f"Images copied: {copied_images}")
    print(f"Labels copied: {copied_labels}")

def main():

    print("\n==============================")
    print(" BUILDING COMBINED DATASET")
    print("==============================")

    reset_combined()

    for dataset_name in DATASETS:
        copy_dataset(dataset_name)

    print("\n==============================")
    print(" COMBINATION COMPLETE")
    print("==============================")

    for split in ["train", "val", "test"]:

        image_count = len(
            list((COMBINED_ROOT / "images" / split).iterdir())
        )

        label_count = len(
            list((COMBINED_ROOT / "labels" / split).iterdir())
        )

        print(
            f"{split.upper():5} "
            f"Images: {image_count:6} | "
            f"Labels: {label_count:6}"
        )


if __name__ == "__main__":
    main()