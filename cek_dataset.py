
from pathlib import Path

DATASET = Path("dataset_v1")
SPLITS = ["train", "val", "test"]
CLASS_NAMES = {
    0: "pita_biru",
    1: "pita_putih",
    2: "pita_hijau",
}

errors = []
total_images = 0
total_labels = 0

for split in SPLITS:
    image_dir = DATASET / "images" / split
    label_dir = DATASET / "labels" / split

    images = [
        p for p in image_dir.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    ]

    print(f"\n--- {split.upper()} ---")
    print(f"Jumlah gambar: {len(images)}")
    total_images += len(images)

    for image in images:
        label = label_dir / f"{image.stem}.txt"

        if not label.exists():
            errors.append(f"Label tidak ditemukan: {image.name}")
            continue

        total_labels += 1
        lines = label.read_text(encoding="utf-8").splitlines()

        if not lines:
            errors.append(f"Label kosong: {label}")

        for line_no, line in enumerate(lines, start=1):
            parts = line.split()

            if len(parts) != 5:
                errors.append(f"Format salah: {label}, baris {line_no}")
                continue

            try:
                class_id = int(parts[0])
                coords = [float(x) for x in parts[1:]]
            except ValueError:
                errors.append(f"Nilai bukan angka: {label}, baris {line_no}")
                continue

            if class_id not in CLASS_NAMES:
                errors.append(f"ID kelas tidak valid: {label}, baris {line_no}")

            if any(x < 0 or x > 1 for x in coords):
                errors.append(f"Koordinat di luar 0-1: {label}, baris {line_no}")

print("\n===== RINGKASAN =====")
print(f"Total gambar: {total_images}")
print(f"Total file label ditemukan: {total_labels}")
print(f"Jumlah masalah: {len(errors)}")

if errors:
    print("\nDaftar masalah (maksimal 30):")
    for error in errors[:30]:
        print("-", error)
else:
    print("Pemeriksaan format dasar berhasil!")
