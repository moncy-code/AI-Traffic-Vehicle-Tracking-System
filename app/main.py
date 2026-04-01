from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import schemas, crud
from app.prediction import predict_next_camera

app = FastAPI(title="Smart Vehicle Tracking System")

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Vehicle Tracking API is running"}


@app.post("/cameras", response_model=schemas.CameraResponse)
def add_camera(camera: schemas.CameraCreate, db: Session = Depends(get_db)):
    return crud.create_camera(db, camera)


@app.get("/cameras", response_model=list[schemas.CameraResponse])
def read_cameras(db: Session = Depends(get_db)):
    return crud.get_cameras(db)


@app.post("/events", response_model=schemas.VehicleEventResponse)
def add_vehicle_event(event: schemas.VehicleEventCreate, db: Session = Depends(get_db)):
    return crud.create_vehicle_event(db, event)


@app.get("/vehicle/{plate_number}", response_model=list[schemas.VehicleEventResponse])
def get_vehicle_history(plate_number: str, db: Session = Depends(get_db)):
    events = crud.get_vehicle_history(db, plate_number)
    if not events:
        raise HTTPException(status_code=404, detail="No sightings found for this plate number")
    return events


@app.get("/vehicle/{plate_number}/last-seen", response_model=schemas.VehicleEventResponse)
def get_last_seen(plate_number: str, db: Session = Depends(get_db)):
    event = crud.get_last_seen(db, plate_number)
    if not event:
        raise HTTPException(status_code=404, detail="No sightings found for this plate number")
    return event

@app.get("/vehicle/{plate_number}/predict")
def predict_vehicle_route(plate_number: str, db: Session = Depends(get_db)):
    events = crud.get_vehicle_history(db, plate_number)

    if not events or len(events) < 2:
        raise HTTPException(status_code=400, detail="Not enough data to predict")

    # convert SQLAlchemy objects to dict
    event_list = [
        {
            "camera_id": e.camera_id,
            "timestamp": e.timestamp
        }
        for e in reversed(events)  # oldest → newest
    ]

    prediction = predict_next_camera(event_list)

    if not prediction:
        raise HTTPException(status_code=400, detail="No prediction available")

    return prediction