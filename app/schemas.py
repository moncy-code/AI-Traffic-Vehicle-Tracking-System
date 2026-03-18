from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CameraBase(BaseModel):
    camera_id: str
    location_name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    connected_to: Optional[str] = None


class CameraCreate(CameraBase):
    pass


class CameraResponse(CameraBase):
    id: int

    class Config:
        from_attributes = True


class VehicleEventBase(BaseModel):
    plate_number: str
    camera_id: str
    vehicle_confidence: Optional[float] = None
    ocr_confidence: Optional[float] = None
    vehicle_image_path: Optional[str] = None
    plate_image_path: Optional[str] = None


class VehicleEventCreate(VehicleEventBase):
    pass


class VehicleEventResponse(VehicleEventBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True