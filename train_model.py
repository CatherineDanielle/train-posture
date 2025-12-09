from ultralytics import YOLO
import os

def main():
    DATA = "dataset/data.yaml"

    # Load YOLOv8m model (MAKE SURE yolov8m.pt exists!)
    model = YOLO("yolov8m.pt")

    model.train(
        data=DATA,
        epochs=50,
        imgsz=640,
        batch=8,
        project="runs/posture",
        name="posture_detector",
        exist_ok=True
    )

    best_model = "runs/posture/posture_detector/weights/best.pt"

    if os.path.exists(best_model):
        print("Copying best model to root folder...")
        os.system(f'copy "{best_model}" "best_posture_detector.pt"')
        print("Done! Saved as best_posture_detector.pt")
    else:
        print("❌ best.pt tidak ditemukan. Cek folder runs/posture/posture_detector/weights/")

if __name__ == "__main__":
    main()
