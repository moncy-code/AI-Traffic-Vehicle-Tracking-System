from ultralytics import YOLO
import cv2


class PlateDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect_objects(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or cannot be read")

        results = self.model(image_path)
        detections = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0].item())
                cls = int(box.cls[0].item())

                detections.append({
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "confidence": conf,
                    "class_id": cls
                })

        return image, detections