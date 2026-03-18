from detection.ocr import PlateOCR
import requests
import datetime

API_URL = "http://127.0.0.1:8000"


class DetectionPipeline:
    def __init__(self):
        self.ocr = PlateOCR()

    def process_image(self, image_path, camera_id="CAM_01"):
        # Step 1: OCR
        plate_text, confidence = self.ocr.read_plate(image_path)

        print(f"Detected Plate: {plate_text} (conf: {confidence})")

        if plate_text == "":
            print("No plate detected.")
            return

        # Step 2: Prepare data
        data = {
            "plate_number": plate_text,
            "camera_id": camera_id,
            "vehicle_confidence": 1.0,
            "ocr_confidence": confidence,
            "vehicle_image_path": image_path,
            "plate_image_path": image_path
        }

        # Step 3: Send to backend
        response = requests.post(f"{API_URL}/events", json=data)

        if response.status_code == 200:
            print("✅ Event saved to database")
        else:
            print("❌ Failed to save:", response.text)