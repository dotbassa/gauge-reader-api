import os
from dotenv import load_dotenv

load_dotenv()

# MQTT Configuration
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")

# Camera Configuration
DEVICE_NAME = os.getenv("CAMERA_DEVICE_NAME")
# Warning Thresholds
WARNING_THRESHOLD_LOW = float(os.getenv("WARNING_THRESHOLD_LOW", "10.0"))
WARNING_THRESHOLD_HIGH = float(os.getenv("WARNING_THRESHOLD_HIGH", "90.0"))
