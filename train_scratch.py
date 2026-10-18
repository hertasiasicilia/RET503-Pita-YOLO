
from pathlib import Path
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent


def main():
    # Membuat model dari konfigurasi, tanpa bobot pretrained
    model = YOLO("yolo26n.yaml")

    model.train(
        data=str(BASE_DIR / "dataset_v1" / "data.yaml"),
        epochs=50,
        imgsz=640,
        batch=8,
        patience=10,
        workers=0,
        project=str(BASE_DIR / "runs" / "pita"),
        name="exp2_scratch",
        exist_ok=False,
        plots=True,
        pretrained=False,
        seed=0,
    )


if __name__ == "__main__":
    main()
