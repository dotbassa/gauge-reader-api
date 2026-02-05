from typing import Optional
from app.services.mqtt_service import MQTTService


class MQTTManager:
    """Manages MQTT connection and provides a simple interface."""

    def __init__(self):
        self.mqtt_service = MQTTService()

    def start(self):
        """Start the MQTT service."""
        if self.mqtt_service.connect():
            self.mqtt_service.start_loop()
            print("MQTT Manager started successfully")
            return True
        else:
            print("Failed to start MQTT Manager")
            return False

    def stop(self):
        """Stop the MQTT service."""
        self.mqtt_service.stop_loop()
        self.mqtt_service.disconnect()
        print("MQTT Manager stopped")

    def get_latest_reading(self) -> Optional[dict]:
        """Get the latest gauge reading."""
        return self.mqtt_service.get_latest_reading()

    def get_raw_data(self) -> Optional[dict]:
        """Get the latest raw camera data."""
        return self.mqtt_service.get_raw_data()

    def is_connected(self) -> bool:
        """Check if MQTT is connected."""
        return self.mqtt_service.is_connected()


mqtt_manager = MQTTManager()
