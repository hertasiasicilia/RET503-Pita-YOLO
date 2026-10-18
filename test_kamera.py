
import cv2

kamera = cv2.VideoCapture(0)

if not kamera.isOpened():
    print("Kamera tidak dapat dibuka.")
    print("Periksa izin kamera atau tutup aplikasi lain yang menggunakannya.")
    raise SystemExit

print("Kamera berhasil dibuka!")
print("Tekan Q pada jendela kamera untuk keluar.")

while True:
    berhasil, frame = kamera.read()

    if not berhasil:
        print("Gagal mengambil gambar.")
        break

    cv2.imshow("Tes Kamera RET503", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

kamera.release()
cv2.destroyAllWindows()
