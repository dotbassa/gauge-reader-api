import json
import base64
import paho.mqtt.client as mqtt
from app.core.config import (
    MQTT_HOST,
    MQTT_PORT,
    MQTT_TOPIC,
    MQTT_USERNAME,
    MQTT_PASSWORD,
    MQTT_CLIENT_ID,
)


class MQTTService:
    def __init__(self):
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID)
        self.client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
        self.client.on_connect = self._on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self._on_disconnect

        self.connected = False
        self.latest_reading = None

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the MQTT broker."""
        if rc == 0:
            print(f"Connected to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
            self.connected = True
            client.subscribe(MQTT_TOPIC, qos=1)
            print(f"Subscribed to topic: {MQTT_TOPIC}")
        else:
            print(f"Failed to connect to MQTT broker. Return code: {rc}")
            self.connected = False

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects."""
        print(f"Disconnected from MQTT broker. Return code: {rc}")
        self.connected = False

    def on_message(self, client, userdata, msg):
        """Handle incoming MQTT messages."""
        [print("\n", "-" * 50, "\n")]
        print(f"Received message on topic: {msg.topic}")
        print(f"Message size: {len(msg.payload)} bytes")

        data = json.loads(msg.payload.decode())

        debug_data = data.copy()
        if "values" in debug_data and "image" in debug_data["values"]:
            image_data = debug_data["values"]["image"]
            debug_data["values"][
                "image"
            ] = f"{image_data[:50]}... (truncated, length: {len(image_data)})"

        if "values" in data:
            values = data["values"]
            print(f"Camera: {values.get('devName')}")
            print(f"Battery: {values.get('battery')}%")
            print(f"Capture: {values.get('snapType')} at {values.get('localtime')}")
            print(f"Image size: {values.get('imageSize')} bytes")

            if "image" in values and values["image"]:
                print("Received image from camera!")

                try:
                    if image_data.startswith("data:image/jpeg;base64,"):
                        base64_data = image_data.replace("data:image/jpeg;base64,", "")

                        missing_padding = len(base64_data) % 4
                        if missing_padding:
                            base64_data += "=" * (4 - missing_padding)

                        image_bytes = base64.b64decode(base64_data)
                        print(f"Decoded image: {len(image_bytes)} bytes")

                        # TODO: replace with actual image processing using image_bytes
                        mock_result = {
                            "success": True,
                            "result": {
                                "value": 75.5,  # mock gauge value
                                "confidence": 0.95,  # mock confidence
                            },
                        }

                        self.latest_reading = {
                            "timestamp": data.get("ts"),
                            "device_name": values.get("devName"),
                            "device_mac": values.get("devMac"),
                            "battery": values.get("battery"),
                            "snap_type": values.get("snapType"),
                            "local_time": values.get("localtime"),
                            "image_size": values.get("imageSize"),
                            "decoded_image_size": len(image_bytes),
                            "result": mock_result,
                        }

                        print(
                            f"Stored camera reading: {mock_result['result']['value']}"
                        )
                        print(
                            f"Ready for image processing with {len(image_bytes)} bytes of image data"
                        )

                    else:
                        print(f"Unexpected image format: {image_data[:50]}...")

                except Exception as e:
                    print(f"Error processing image: {e}")
                    import traceback

                    traceback.print_exc()
            else:
                print("No image data in camera message")

    def get_latest_reading(self):
        """Get the latest gauge reading."""
        return self.latest_reading

    def connect(self):
        """Connect to the MQTT broker."""
        try:
            print(f"Connecting to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
            self.client.connect(MQTT_HOST, MQTT_PORT, 60)
            return True
        except Exception as e:
            print(f"Error connecting to MQTT broker: {e}")
            return False

    def start_loop(self):
        """Start the MQTT client loop."""
        self.client.loop_start()

    def stop_loop(self):
        """Stop the MQTT client loop."""
        self.client.loop_stop()

    def disconnect(self):
        """Disconnect from the MQTT broker."""
        self.client.disconnect()

    def is_connected(self) -> bool:
        """Check if connected to MQTT broker."""
        return self.connected
