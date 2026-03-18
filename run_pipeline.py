from detection.pipeline import DetectionPipeline

pipeline = DetectionPipeline()

pipeline.process_image("test_plate.jpg", camera_id="CAM_01")