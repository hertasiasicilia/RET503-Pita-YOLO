import cv2
import argparse
from pathlib import Path

CLASS_BY_ID = {0: "pita_biru", 1: "pita_putih", 2: "pita_hijau"}
KEY_CLASSES = {
    ord("1"): (0, "pita_biru"),
    ord("2"): (1, "pita_putih"),
    ord("3"): (2, "pita_hijau"),
}

image = None
boxes = []
drawing = False
start_point = None
current_box = None
scale = 1.0
active_class_id = 0
active_class_name = "pita_biru"


def mouse_callback(event, x, y, flags, param):
    global drawing, start_point, current_box, boxes
    if image is None:
        return
    h, w = image.shape[:2]
    ox = max(0, min(int(x / scale), w - 1))
    oy = max(0, min(int(y / scale), h - 1))

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (ox, oy)
        current_box = None
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        current_box = (start_point[0], start_point[1], ox, oy)
    elif event == cv2.EVENT_LBUTTONUP and drawing:
        drawing = False
        x1, y1 = start_point
        x2, y2 = ox, oy
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        if x2 - x1 >= 3 and y2 - y1 >= 3:
            boxes.append((active_class_id, x1, y1, x2, y2))
        current_box = None


def save_label(path, shape, annotations):
    h, w = shape[:2]
    lines = []
    for cid, x1, y1, x2, y2 in annotations:
        cx = ((x1 + x2) / 2) / w
        cy = ((y1 + y2) / 2) / h
        bw = (x2 - x1) / w
        bh = (y2 - y1) / h
        lines.append(f"{cid} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def main():
    global image, boxes, drawing, start_point, current_box
    global scale, active_class_id, active_class_name

    parser = argparse.ArgumentParser()
    parser.add_argument("--kelas", choices=["pita_biru", "pita_putih", "pita_hijau"], required=True)
    parser.add_argument("--folder", default="dataset_raw")
    parser.add_argument("--labels", default="labels_raw")
    args = parser.parse_args()

    source = Path(args.folder) / args.kelas
    output = Path(args.labels) / args.kelas
    if not source.exists():
        print(f"Folder tidak ditemukan: {source.resolve()}")
        return

    files = sorted(p for p in source.iterdir()
                   if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp", ".webp"})
    if not files:
        print(f"Tidak ada foto di {source.resolve()}")
        return

    active_class_id = {"pita_biru": 0, "pita_putih": 1, "pita_hijau": 2}[args.kelas]
    active_class_name = args.kelas
    window = "Anotasi Pita YOLO"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window, mouse_callback)

    i = 0
    while i < len(files):
        path = files[i]
        image = cv2.imread(str(path))
        if image is None:
            print(f"Lewati foto rusak: {path.name}")
            i += 1
            continue
        label_path = output / f"{path.stem}.txt"
        boxes = []
        drawing = False
        start_point = None
        current_box = None

        # Muat label yang sudah ada agar bisa diperiksa tanpa mengulang dari nol.
        if label_path.exists():
            h, w = image.shape[:2]
            try:
                for line in label_path.read_text(encoding="utf-8").splitlines():
                    p = line.split()
                    if len(p) != 5:
                        continue
                    cid = int(p[0])
                    cx, cy, bw, bh = map(float, p[1:])
                    boxes.append((cid, int((cx-bw/2)*w), int((cy-bh/2)*h),
                                  int((cx+bw/2)*w), int((cy+bh/2)*h)))
            except Exception:
                boxes = []

        while True:
            canvas = image.copy()
            for cid, x1, y1, x2, y2 in boxes:
                cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 220, 0), 2)
                cv2.putText(canvas, CLASS_BY_ID.get(cid, str(cid)), (x1, max(20, y1-6)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 0), 2)
            if current_box:
                x1, y1, x2, y2 = current_box
                cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 200, 255), 2)

            h, w = canvas.shape[:2]
            scale = min(1100 / w, 720 / h, 1.0)
            if scale < 1:
                canvas = cv2.resize(canvas, (int(w*scale), int(h*scale)))
            cv2.putText(canvas, f"Kelas aktif: {active_class_name} | Kotak: {len(boxes)}",
                        (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
            cv2.putText(canvas, "1=Biru 2=Putih 3=Hijau | S=Simpan+Next | U=Undo | C=Clear | Q=Keluar",
                        (12, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 0, 255), 2)
            cv2.imshow(window, canvas)
            key = cv2.waitKey(20) & 0xFF

            if key in KEY_CLASSES:
                active_class_id, active_class_name = KEY_CLASSES[key]
            elif key in (ord("u"), ord("U")):
                if boxes:
                    boxes.pop()
            elif key in (ord("c"), ord("C")):
                boxes.clear()
            elif key in (ord("s"), ord("S"), 13):
                save_label(label_path, image.shape, boxes)
                print(f"[{i+1}/{len(files)}] {path.name} -> {label_path}")
                i += 1
                break
            elif key in (ord("b"), ord("B")):
                i = max(0, i-1)
                break
            elif key in (ord("q"), ord("Q"), 27):
                print("Keluar. Label yang sudah disimpan tetap aman.")
                cv2.destroyAllWindows()
                return

    cv2.destroyAllWindows()
    print(f"Selesai. Label disimpan di {output.resolve()}")


if __name__ == "__main__":
    main()
