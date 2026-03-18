from sqlalchemy.orm import Session
from app import models, schemas


def create_camera(db: Session, camera: schemas.CameraCreate):
    db_camera = models.Camera(**camera.model_dump())
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera


def get_cameras(db: Session):
    return db.query(models.Camera).all()


def create_vehicle_event(db: Session, event: schemas.VehicleEventCreate):
    db_event = models.VehicleEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_vehicle_history(db: Session, plate_number: str):
    return (
        db.query(models.VehicleEvent)
        .filter(models.VehicleEvent.plate_number == plate_number)
        .order_by(models.VehicleEvent.timestamp.desc())
        .all()
    )


def get_last_seen(db: Session, plate_number: str):
    return (
        db.query(models.VehicleEvent)
        .filter(models.VehicleEvent.plate_number == plate_number)
        .order_by(models.VehicleEvent.timestamp.desc())
        .first()
    )