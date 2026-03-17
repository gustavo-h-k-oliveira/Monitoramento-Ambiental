from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.database.db import get_latest_data, get_average_data
from app.models.metrics import Metric

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"]
)

def row_to_dict(row):
    return {
        "device_id": row["device_id"],
        "temperature": row["temperature"],
        "humidity": row["humidity"],
        "lux": row["lux"],
        "time": row["time"].isoformat()
    }

@router.get("/latest", response_model=List[dict])
def get_latest():
    try:
        rows = get_latest_data()
        return [row_to_dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/average/")
def get_average(metric: Metric = Query(...)):
    try:
        rows = get_average_data(metric)
        return [{"bucket": r["bucket"], "avg": float(r["avg"])} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    