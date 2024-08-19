
from app.core import errors
import logging

from app.core.furniture_segmentation_service import FurnitureSegmentationService
from app.config.config import config
import roboflow

from app.io.gateway.furniture_segmentation_gateway import FurnitureSegmentationGateway

logger = logging.getLogger(__name__)

furniture_segmentation_service: FurnitureSegmentationService = None


async def initialize_furniture_segmentation_service():
    global furniture_segmentation_service

    try:

        rf = roboflow.Roboflow(api_key=config.gateway.ROBOFLOW_API_KEY)
        project = rf.workspace().project(config.gateway.ROBOFLOW_PROJECT_NAME)
        remote_ml_model = project.version(config.gateway.ROBOFLOW_MODEL_VERSION).model
        remote_ml_model.confidence = config.ml_model.MODEL_CONFIDENCE
        remote_ml_model.overlap = config.ml_model.MODEL_OVERLAP

        logger.info(f"Инициализация модели: {config.ml_model.MODEL_NAME}")

        furniture_segmentation_gateway = FurnitureSegmentationGateway(remote_ml_model)

        furniture_segmentation_service = FurnitureSegmentationService(furniture_segmentation_gateway)

        logger.debug("Сервис успешно инициализирован")

    except Exception as e:
        logger.error(f"Ошибка при инициализации сервиса: {e}")
        raise errors.ServiceInitializationError("Не удалось инициализировать сервис")


def get_furniture_segmentation_service() -> FurnitureSegmentationService:
    if furniture_segmentation_service is None:
        logger.error(
            "Сервис не инициализирован")
        raise errors.ServiceInitializationError(
            "Сервис не инициализирован")

    return furniture_segmentation_service
