from pathlib import Path
import random
import shutil
from collections import Counter

SOURCE = Path("datasets/combined")
DEST = Path("datasets/combined_v2")

SEED = 42
random.seed(SEED)

CLASS_NAMES = {
    0: "pothole",
    1: "crack",
    2: "trash",
    3: "rock",
    4: "tree",
    5: "branch",
    6: "light_pole",
}

# --------------------------------------------------
# COLLECT ALL IMAGE/LABEL PAIRS FROM CURRENT DATASET
# --------------------------------------------------

pairs = {}

for split in ["train", "val", "test"]:
    label_dir = SOURCE / "labels" / split
    image_dir = SOURCE / "images" / split

    for label_path in label_dir.glob("*.txt"):
        base_name = label_path.stem
        image_path = None

        for ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            candidate = image_dir / f"{base_name}{ext}"

            if candidate.exists():
                image_path = candidate
                break

        if image_path is None:
            print(f"WARNING: No image found for {label_path}")
            continue

        pairs[base_name] = (image_path, label_path)

pairs = list(pairs.values())

print(f"Found {len(pairs)} image/label pairs.")

# --------------------------------------------------
# FIND WHICH CLASSES ARE IN EACH IMAGE
# --------------------------------------------------

items = []

for image_path, label_path in pairs:
    classes = set()

    with open(label_path, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            class_id = int(line.split()[0])
            classes.add(class_id)

    items.append({
        "image": image_path,
        "label": label_path,
        "classes": classes
    })

# --------------------------------------------------
# COUNT IMAGES PER CLASS
# --------------------------------------------------

class_image_counts = Counter()

for item in items:
    for class_id in item["classes"]:
        class_image_counts[class_id] += 1

print("\nImages containing each class:")

for class_id in range(7):
    print(
        f"{class_id} {CLASS_NAMES[class_id]:<12} "
        f"{class_image_counts[class_id]}"
    )

# --------------------------------------------------
# PROCESS RARE CLASSES FIRST
# --------------------------------------------------

items.sort(
    key=lambda item: min(
        class_image_counts[c] for c in item["classes"]
    ) if item["classes"] else 999999
)

train = []
val = []
test = []

split_class_counts = {
    "train": Counter(),
    "val": Counter(),
    "test": Counter()
}

ratios = {
    "train": 0.80,
    "val": 0.10,
    "test": 0.10
}

# --------------------------------------------------
# ASSIGN EACH IMAGE TO A SPLIT
# --------------------------------------------------

for item in items:
    scores = {}

    for split_name, ratio in ratios.items():
        score = 0

        for class_id in item["classes"]:
            target = class_image_counts[class_id] * ratio
            current = split_class_counts[split_name][class_id]

            if target > 0:
                score += current / target

        scores[split_name] = score

    chosen = min(scores, key=scores.get)

    if chosen == "train":
        train.append(item)
    elif chosen == "val":
        val.append(item)
    else:
        test.append(item)

    for class_id in item["classes"]:
        split_class_counts[chosen][class_id] += 1

random.shuffle(train)
random.shuffle(val)
random.shuffle(test)

# --------------------------------------------------
# COPY FILES
# --------------------------------------------------

def copy_split(split_items, split_name):
    image_dest = DEST / "images" / split_name
    label_dest = DEST / "labels" / split_name

    for item in split_items:
        shutil.copy2(
            item["image"],
            image_dest / item["image"].name
        )

        shutil.copy2(
            item["label"],
            label_dest / item["label"].name
        )

print("\nCopying files...")

copy_split(train, "train")
copy_split(val, "val")
copy_split(test, "test")

# --------------------------------------------------
# PRINT RESULTS
# --------------------------------------------------

print("\nV2 SPLIT COMPLETE")
print("-" * 50)

print(f"Train: {len(train)}")
print(f"Val:   {len(val)}")
print(f"Test:  {len(test)}")

print("\nCLASS DISTRIBUTION BY IMAGE")
print("-" * 50)

for class_id in range(7):
    print(
        f"{CLASS_NAMES[class_id]:<12} "
        f"train={split_class_counts['train'][class_id]:<6} "
        f"val={split_class_counts['val'][class_id]:<6} "
        f"test={split_class_counts['test'][class_id]:<6}"
    )