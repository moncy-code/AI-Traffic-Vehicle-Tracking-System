from detection.pipeline import DetectionPipeline

pipeline = DetectionPipeline()

pipeline.process_image("test_plate.jpg", camera_id="CAM_01")
pipeline.process_image("test_plate.jpg", camera_id="CAM_02")
pipeline.process_image("test_plate.jpg", camera_id="CAM_03")
pipeline.process_image("test_plate.jpg", camera_id="CAM_02")
pipeline.process_image("test_plate.jpg", camera_id="CAM_03")
pipeline.process_image("test_plate.jpg", camera_id="CAM_04")