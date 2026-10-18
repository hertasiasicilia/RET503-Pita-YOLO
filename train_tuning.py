
from pathlib import Path
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent


def main():
    model = YOLO("yolo26n.pt")

    model.train(
        data=str(BASE_DIR / "dataset_v1" / "data.yaml"),
        epochs=50,
        imgsz=640,
        batch=4,
        patience=10,
        workers=0,
        project=str(BASE_DIR / "runs" / "pita"),
        name="exp3_tuning",
        exist_ok=False,
        plots=True,
        seed=0,
    )


if __name__ == "__main__":
    main()
