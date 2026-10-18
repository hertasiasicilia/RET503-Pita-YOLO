
from pathlib import Path
from ultralytics import YOLO

# Folder utama proyek, berdasarkan lokasi file ini
BASE_DIR = Path(__file__).resolve().parent


def main():
    # Model pretrained untuk transfer learning
    model = YOLO("yolo26n.pt")

    # Training deteksi pita
    model.train(
        data=str(BASE_DIR / "dataset_v1" / "data.yaml"),
        epochs=50,
        imgsz=640,
        batch=8,
        patience=10,
        workers=0,
        project=str(BASE_DIR / "runs" / "pita"),
        name="exp1_pretrained",
        exist_ok=True,
        plots=True,
    )


if __name__ == "__main__":
    main()
