import time
import cv2
import numpy as np
from datetime import datetime
from typing import Dict, Any
from app.schemas.gauge_reader import GaugeReadingResponse


class GaugeProcessingService:

    def __init__(self):
        pass

    def process_gauge_image(
        self, image_bytes: bytes, metadata: Dict[str, Any] = None
    ) -> GaugeReadingResponse:
        pass
