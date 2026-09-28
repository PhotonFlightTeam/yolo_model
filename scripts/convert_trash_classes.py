from pathlib import Path

DATASET_ROOT = Path("datasets/raw/trash")
GLOBAL_TRASH_CLASS = 2

label_files = [
    file
    for file in DATASET_ROOT.rglob("*.txt")
    if "labels" in [part.lower() for part in file.parts]
]

converted_objects = 0

for label_file in label_files:
    new_lines = []

    with open(label_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) != 5:
                print(f"Skipping invalid line in {label_file}: {line}")
                continue

            # Replace the original local class ID with global trash class 2
            parts[0] = str(GLOBAL_TRASH_CLASS)

            new_lines.append(" ".join(parts))
            converted_objects += 1

    with open(label_file, "w", encoding="utf-8") as file:
        if new_lines:
            file.write("\n".join(new_lines) + "\n")


print("\n--- TRASH CONVERSION COMPLETE ---")
print(f"Objects converted to global class 2: {converted_objects}")