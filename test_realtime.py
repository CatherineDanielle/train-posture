from ultralytics import YOLO
import cv2

model = YOLO("runs/posture/posture_detector/weights/best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    annotated = results[0].plot()  # draw boxes

    cv2.imshow("Posture Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
