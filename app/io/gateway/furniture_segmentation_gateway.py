import logging
from typing import Dict, Any

from app.core.errors import GatewayError
import roboflow

logger = logging.getLogger(__name__)


class FurnitureSegmentationGateway:

    def __init__(self, remote_ml_model: Any):
        self.remote_ml_model = remote_ml_model
        logger.debug("FurnitureSegmentationGateway проинициализирован")

    async def segment_furniture(self, image: Any) -> Dict:

        try:
            prediction = self.remote_ml_model.predict(image)
            return prediction.json()

        except Exception as e:
            raise GatewayError(500, str(e))
