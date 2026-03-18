import easyocr
import cv2


class PlateOCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def read_plate(self, image_path):
        image = cv2.imread(image_path)

        if image is None:
            raise ValueError("Image not found or cannot be read")

        results = self.reader.readtext(image)

        best_text = ""
        best_conf = 0.0

        for (bbox, text, confidence) in results:
            if confidence > best_conf:
                best_text = text
                best_conf = confidence

        return best_text, best_conf