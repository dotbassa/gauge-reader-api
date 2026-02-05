from fastapi import APIRouter, HTTPException, status
from app.schemas.gauge_reader import GaugeReadingResponse
from app.services.mqtt_manager import mqtt_manager

router = APIRouter()


@router.get("/latest", response_model=GaugeReadingResponse)
async def get_latest_reading():
    """Get the latest gauge reading received via MQTT."""
    try:
        latest = mqtt_manager.get_latest_reading()

        if not latest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No gauge readings available yet",
            )

        if not latest["result"].get("success"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Latest reading failed: {latest['result'].get('error')}",
            )

        if "result" in latest:
            gauge_data = latest["result"]["result"]
            return GaugeReadingResponse(
                value=gauge_data["value"],
                confidence=gauge_data["confidence"],
                timestamp=latest.get("timestamp"),
                device_name=latest.get("device_name"),
                device_mac=latest.get("device_mac"),
                battery=latest.get("battery"),
                snap_type=latest.get("snap_type"),
                local_time=latest.get("local_time"),
                image_size=latest.get("image_size"),
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get latest reading: {str(e)}",
        )


@router.get("/status")
async def get_mqtt_status():
    """Get MQTT connection status."""
    return {
        "mqtt_connected": mqtt_manager.is_connected(),
        "latest_reading_available": mqtt_manager.get_latest_reading() is not None,
    }
