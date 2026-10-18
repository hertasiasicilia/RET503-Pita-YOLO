
import random
import shutil
from pathlib import Path

random.seed(42)

RAW_DIR = Path("dataset_raw")
LABEL_DIR = Path("labels_raw")
OUTPUT_DIR = Path("dataset_v1")

CLASSES = ["pita_biru", "pita_putih", "pita_hijau"]
EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Pembagian: 70% train, 20% validation, 10% test
SPLITS = {
    "train": 0.7,
    "val": 0.2,
    "test": 0.1,
}

for split in SPLITS:
    (OUTPUT_DIR / "images" / split).mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "labels" / split).mkdir(parents=True, exist_ok=True)

total = 0

for class_id, class_name in enumerate(CLASSES):
    image_dir = RAW_DIR / class_name
    label_dir = LABEL_DIR / class_name

    if not image_dir.exists() or not label_dir.exists():
        raise FileNotFoundError(
            f"Folder tidak ditemukan: {image_dir} atau {label_dir}"
        )

    images = sorted(
        p for p in image_dir.iterdir()
        if p.suffix.lower() in EXTENSIONS
    )

    # Hanya gunakan foto yang mempunyai label
    valid_images = [p for p in images if (label_dir / f"{p.stem}.txt").exists()]

    if not valid_images:
        raise ValueError(f"Tidak ada foto berlabel di kelas {class_name}")

    random.shuffle(valid_images)

    n = len(valid_images)
    n_train = int(n * 0.7)
    n_val = int(n * 0.2)

    split_files = {
        "train": valid_images[:n_train],
        "val": valid_images[n_train:n_train + n_val],
        "test": valid_images[n_train + n_val:],
    }

    for split, files in split_files.items():
        for img_path in files:
            # Nama file unik agar antarkelas tidak bertabrakan
            new_stem = f"{class_name}_{img_path.stem}"
            destination_image = OUTPUT_DIR / "images" / split / f"{new_stem}{img_path.suffix.lower()}"
            destination_label = OUTPUT_DIR / "labels" / split / f"{new_stem}.txt"

            shutil.copy2(img_path, destination_image)
            shutil.copy2(label_dir / f"{img_path.stem}.txt", destination_label)

        print(f"{class_name} | {split}: {len(files)} foto")

    total += n

# Buat data.yaml untuk Ultralytics YOLO
yaml_text = """path: dataset_v1
train: images/train
val: images/val
test: images/test

names:
  0: pita_biru
  1: pita_putih
  2: pita_hijau
"""

(OUTPUT_DIR / "data.yaml").write_text(yaml_text, encoding="utf-8")

print(f"\nTotal foto yang dibagi: {total}")
print(f"Dataset tersimpan di: {OUTPUT_DIR.resolve()}")
print("File konfigurasi dibuat: dataset_v1/data.yaml")
