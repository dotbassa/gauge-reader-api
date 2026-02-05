from pydantic import BaseModel
from typing import Optional


class GaugeReadingResponse(BaseModel):
    value: float
    confidence: float
    timestamp: Optional[int] = None
    device_name: Optional[str] = None
    device_mac: Optional[str] = None
    battery: Optional[int] = None
    snap_type: Optional[str] = None
    local_time: Optional[str] = None
    image_size: Optional[int] = None


class GaugeReadingResult(BaseModel):
    success: bool
    result: Optional[GaugeReadingResponse] = None
    error: Optional[str] = None
    timestamp: Optional[int] = None
    device_name: Optional[str] = None
    device_mac: Optional[str] = None
    battery: Optional[int] = None
    snap_type: Optional[str] = None
    local_time: Optional[str] = None
    image_size: Optional[int] = None
