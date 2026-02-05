from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.api import api_router
from app.services.mqtt_manager import mqtt_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Gauge Reader API...")

    if mqtt_manager.start():
        print("MQTT Service started successfully")
    else:
        print("Failed to start MQTT service")

    yield

    print("Shutting down Gauge Reader API...")
    mqtt_manager.stop()


app = FastAPI(
    title="Gauge Reader API", root_path="/gauge-reader-api", lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*\.lco\.cl$",
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(api_router, prefix="/v1")

app.get("/")


async def root():
    return {
        "message": "Gauge Reader API",
        "mqtt_connected": mqtt_manager.is_connected(),
        "docs": "/api/docs",
    }
