from detection.ocr import PlateOCR
import requests
import re

API_URL = "http://127.0.0.1:8000"


def clean_plate_text(text: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", text.upper())


class DetectionPipeline:
    def __init__(self):
        self.ocr = PlateOCR()

    def process_image(self, image_path, camera_id="CAM_01"):
        plate_text, confidence = self.ocr.read_plate(image_path)

        print(f"Raw Detected Plate: {plate_text} (conf: {confidence})")

        cleaned_plate = clean_plate_text(plate_text)

        if cleaned_plate == "":
            print("No valid plate detected.")
            return

        print(f"Cleaned Plate: {cleaned_plate}")

        data = {
            "plate_number": cleaned_plate,
            "camera_id": camera_id,
            "vehicle_confidence": 1.0,
            "ocr_confidence": confidence,
            "vehicle_image_path": image_path,
            "plate_image_path": image_path
        }

        response = requests.post(f"{API_URL}/events", json=data)

        if response.status_code == 200:
            print("✅ Event saved to database")
            print(response.json())
        else:
            print("❌ Failed to save:", response.text)