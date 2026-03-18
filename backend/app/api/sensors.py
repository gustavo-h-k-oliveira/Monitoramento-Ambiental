from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from app.database.db import get_latest_data, get_average_data
from app.models.metrics import Metric
from app.models.hours import Hours

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
def get_latest(
    hours: Hours = Query(Hours.h1, description="Intervalo em horas"),
    to_time: Optional[datetime] = Query(None, description="Instante final (padrão: agora)"),
):
    if to_time is None:
        to_time = datetime.now(timezone.utc)

    from_time = to_time - timedelta(hours=hours.value)

    try:
        rows = get_latest_data(from_time=from_time, to_time=to_time)
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
    