import cv2
import os


def save_cropped_image(image, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)


def crop_image(image, x1, y1, x2, y2):
    return image[y1:y2, x1:x2]