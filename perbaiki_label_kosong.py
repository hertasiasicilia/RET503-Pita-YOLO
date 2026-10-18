
import cv2
from pathlib import Path

CLASS_IDS = {
    "pita_biru": 0,
    "pita_putih": 1,
    "pita_hijau": 2,
}

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main():
    root = Path("dataset_raw")
    labels_root = Path("labels_raw")
    fixed = 0

    for class_name, class_id in CLASS_IDS.items():
        image_folder = root / class_name
        label_folder = labels_root / class_name

        if not image_folder.exists():
            print(f"Folder foto tidak ditemukan: {image_folder}")
            continue

        for photo in sorted(image_folder.iterdir()):
            if photo.suffix.lower() not in EXTENSIONS:
                continue

            label_path = label_folder / f"{photo.stem}.txt"

            # Lewati label yang sudah berisi anotasi.
            if label_path.exists() and label_path.read_text(
                encoding="utf-8"
            ).strip():
                continue

            image = cv2.imread(str(photo))
            if image is None:
                print(f"Foto tidak bisa dibuka: {photo.name}")
                continue

            h, w = image.shape[:2]
            drawing = False
            start = None
            box = None
            boxes = []

            window = f"Anotasi: {photo.name}"
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)

            scale = min(1100 / w, 720 / h, 1.0)
            display = cv2.resize(
                image, (int(w * scale), int(h * scale))
            )

            def mouse(event, x, y, flags, param):
                nonlocal drawing, start, box, boxes

                ox = max(0, min(int(x / scale), w - 1))
                oy = max(0, min(int(y / scale), h - 1))

                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing = True
                    start = (ox, oy)

                elif event == cv2.EVENT_MOUSEMOVE and drawing:
                    box = (start[0], start[1], ox, oy)

                elif event == cv2.EVENT_LBUTTONUP and drawing:
                    drawing = False
                    x1, x2 = sorted((start[0], ox))
                    y1, y2 = sorted((start[1], oy))

                    if x2 - x1 >= 3 and y2 - y1 >= 3:
                        boxes.append((x1, y1, x2, y2))
                    box = None

            cv2.setMouseCallback(window, mouse)

            print(f"\nFoto: {photo.name}")
            print("Tarik kotak mengelilingi pita.")
            print("S = simpan | U = hapus kotak terakhir | Q = berhenti")

            saved = False

            while True:
                canvas = display.copy()

                for x1, y1, x2, y2 in boxes:
                    cv2.rectangle(
                        canvas,
                        (int(x1 * scale), int(y1 * scale)),
                        (int(x2 * scale), int(y2 * scale)),
                        (0, 255, 0), 2
                    )

                if box:
                    x1, y1, x2, y2 = box
                    cv2.rectangle(
                        canvas,
                        (int(x1 * scale), int(y1 * scale)),
                        (int(x2 * scale), int(y2 * scale)),
                        (0, 200, 255), 2
                    )

                cv2.imshow(window, canvas)
                key = cv2.waitKey(20) & 0xFF

                if key in (ord("u"), ord("U")):
                    if boxes:
                        boxes.pop()

                elif key in (ord("s"), ord("S")):
                    if not boxes:
                        print("Kotak masih kosong. Gambar kotak pita dulu.")
                        continue

                    lines = []
                    for x1, y1, x2, y2 in boxes:
                        cx = ((x1 + x2) / 2) / w
                        cy = ((y1 + y2) / 2) / h
                        bw = (x2 - x1) / w
                        bh = (y2 - y1) / h
                        lines.append(
                            f"{class_id} {cx:.6f} {cy:.6f} "
                            f"{bw:.6f} {bh:.6f}"
                        )

                    label_folder.mkdir(parents=True, exist_ok=True)
                    label_path.write_text(
                        "\n".join(lines) + "\n", encoding="utf-8"
                    )

                    print(f"Label tersimpan: {label_path}")
                    fixed += 1
                    saved = True
                    break

                elif key in (ord("q"), ord("Q"), 27):
                    cv2.destroyAllWindows()
                    print("Dihentikan. Kamu bisa melanjutkan nanti.")
                    return

            cv2.destroyWindow(window)

    cv2.destroyAllWindows()
    print(f"\nSelesai! Label kosong yang diperbaiki: {fixed}")


if __name__ == "__main__":
    main()
