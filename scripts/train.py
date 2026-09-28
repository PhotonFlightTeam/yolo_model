from ultralytics import YOLO


def main():
    model = YOLO("yolo11n.pt")

    model.train(
        data="data.yaml",
        epochs=100,
	patience=20,
        imgsz=640,
        batch=32,
        device=0,
        workers=8,
        project="runs",
        name="multi_anomaly_full"
    )


if __name__ == "__main__":
    main()