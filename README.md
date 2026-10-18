# RET503 - Deteksi Pita Menggunakan YOLO26n

## 1. Deskripsi Proyek
Proyek ini menggunakan model YOLO26n untuk mendeteksi tiga kelas pita:
- Pita biru (`pita_biru`)
- Pita putih (`pita_putih`)
- Pita hijau (`pita_hijau`)

## 2. Dataset
Dataset berisi 150 gambar dengan pembagian:
- Training: 105 gambar
- Validasi: 30 gambar
- Test: 15 gambar

## 3. Eksperimen
### E1 - Baseline
- Model: YOLO26n pretrained
- Image size: 640
- Batch: 8
- Epoch terbaik berdasarkan mAP50-95 validasi: 34

### E3 - Tuning
- Model: YOLO26n pretrained
- Image size: 640
- Batch: 4
- Epoch terbaik berdasarkan mAP50-95 validasi: 29

## 4. Hasil Validasi

| Metrik | E1 | E3 |
|---|---:|---:|
| Precision | 95.46% | 95.71% |
| Recall | 96.67% | 96.67% |
| mAP50 | 96.21% | 95.84% |
| mAP50-95 | 61.40% | 62.13% |

## 5. Hasil Test

| Metrik | E1 | E3 |
|---|---:|---:|
| Precision | 98.45% | 98.20% |
| Recall | 100.00% | 93.30% |
| mAP50 | 99.50% | 98.40% |
| mAP50-95 | 60.45% | 60.10% |

Data test terdiri dari 15 gambar, lima gambar per kelas. Hasil ini
merupakan evaluasi awal dan belum mewakili semua variasi kondisi nyata.

## 6. Kesimpulan
E3 memperoleh mAP50-95 validasi sedikit lebih tinggi. Namun, E1
memperoleh hasil test yang sedikit lebih baik pada keempat metrik.
Oleh karena itu, E1 dipilih sebagai kandidat model utama berdasarkan
hasil test yang tersedia.

Pengujian tambahan diperlukan untuk menilai pengaruh latar belakang,
pencahayaan, jarak, dan posisi pita.

## 7. Struktur Hasil

- `dataset_v1/`: dataset yang telah dibagi menjadi training, validasi, dan test.
- `runs/pita/exp1_pretrained/`: hasil eksperimen E1.
- `runs/pita/exp3_tuning/`: hasil eksperimen E3.
- `runs/pita/evaluasi_test_E3/`: hasil evaluasi test E3.
- `runs/pita/perbandingan_E1_E3.csv`: tabel perbandingan validasi.
- `hasil_praktik_4222401029.txt`: ringkasan hasil praktik.

Setiap folder eksperimen memuat grafik training, hasil evaluasi, konfigurasi,
dan bobot model apabila proses training berhasil menyimpannya.

## 8. Lingkungan
- Python 3.14.4
- Ultralytics 8.4.182
- PyTorch CPU
- Model: YOLO26n
