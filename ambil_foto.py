
import cv2
import time
from pathlib import Path
import argparse

# Pengaturan dataset
TARGET_FOTO = 50
INTERVAL = 0.5

parser = argparse.ArgumentParser()
parser.add_argument(
    "--kelas",
    required=True,
    choices=["pita_biru", "pita_putih", "pita_hijau"]
)
args = parser.parse_args()

folder = Path("dataset_raw") / args.kelas
folder.mkdir(parents=True, exist_ok=True)

# Hitung foto yang sudah ada
jumlah = len(list(folder.glob("*.jpg")))

if jumlah >= TARGET_FOTO:
    print(f"Folder {args.kelas} sudah memiliki {jumlah} foto.")
    print("Hapus atau pindahkan foto jika ingin mengambil ulang.")
    raise SystemExit

kamera = cv2.VideoCapture(0)

if not kamera.isOpened():
    print("Kamera gagal dibuka.")
    raise SystemExit

waktu_berikutnya = time.time() + 3

print(f"Kelas: {args.kelas}")
print(f"Target: {TARGET_FOTO} foto")
print("Bersiap selama 3 detik...")
print("Gerakkan pita di depan kamera.")
print("Tekan Q untuk berhenti lebih awal.")

while jumlah < TARGET_FOTO:
    berhasil, frame = kamera.read()

    if not berhasil:
        print("Gagal mengambil gambar.")
        break

    sekarang = time.time()
    tampilan = frame.copy()

    if sekarang >= waktu_berikutnya:
        nama_file = folder / f"{args.kelas}_{jumlah + 1:04d}.jpg"

        if cv2.imwrite(str(nama_file), frame):
            jumlah += 1
            print(f"Foto {jumlah}/{TARGET_FOTO} tersimpan.")

        waktu_berikutnya = time.time() + INTERVAL

    cv2.putText(
        tampilan,
        f"Kelas: {args.kelas} | Foto: {jumlah}/{TARGET_FOTO}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        tampilan,
        "Gerakkan pita | Q = Berhenti",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2
    )

    cv2.imshow("Pengambilan Dataset Pita", tampilan)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

kamera.release()
cv2.destroyAllWindows()

print(f"Selesai! Total foto di folder: {jumlah}/{TARGET_FOTO}")
