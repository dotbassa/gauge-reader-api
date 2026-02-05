from fastapi import APIRouter
from app.api.v1.endpoints import (
    gauge_reader,
)

api_router = APIRouter()

api_router.include_router(
    gauge_reader.router,
    prefix="",
    tags=["gauge-reader"],
)
