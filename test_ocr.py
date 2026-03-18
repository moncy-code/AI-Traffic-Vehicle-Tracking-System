from detection.ocr import PlateOCR

ocr = PlateOCR()

text, conf = ocr.read_plate("test_plate.jpg")

print("Detected Plate:", text)
print("Confidence:", conf)