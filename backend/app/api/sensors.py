from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.database.db import get_db, get_latest_data, get_average_temp

router = APIRouter(
    prefix="/sensors",
    tags=["sensors"]
)

def row_to_dict(row):
    return {
        # "id": row["id"],
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

# @router.get("/average/")
# def get_average():
#     try:
#         rows = get_average_temp()
#         return [{"bucket": r["bucket"], "avg_temp": float(r["avg_temp"])} for r in rows]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    