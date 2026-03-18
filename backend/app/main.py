from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading

from app.mqtt.consumer import start_mqtt_consumer
from app.api import sensors

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Backend iniciado")
    mqtt_thread = threading.Thread(
        target=start_mqtt_consumer,
        daemon=True
    )
    mqtt_thread.start()

    yield

    print("Backend finalizado")

app = FastAPI(
    title="Monitoramento de Ambiente",
    version="0.6",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(sensors.router)
