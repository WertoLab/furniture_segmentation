from typing import Any, Dict, List
import logging
from app.core import schemas
import cv2
from imutils import paths
import numpy as np
from PIL import Image
from app.io.gateway.furniture_segmentation_gateway import FurnitureSegmentationGateway

logger = logging.getLogger(__name__)


class FurnitureSegmentationService:
    def __init__(self, furniture_segmentation_gateway: FurnitureSegmentationGateway):
        self.furniture_segmentation_gateway = furniture_segmentation_gateway
        logger.debug("FurnitureSegmentationService проинициализирован")

    async def _process_model_output(self, model_output: Dict, input_image: str) -> Any:
        input_image = cv2.cvtColor(cv2.imread(input_image), cv2.COLOR_BGR2RGB)
        if not model_output['predictions']:
            return np.zeros(shape=(input_image.shape[1], input_image.shape[0]))
        boxes = model_output['predictions'][0]

        x_upper = boxes['x'] - boxes['width'] / 2
        y_upper = boxes['y'] - boxes['height'] / 2
        x_lower = boxes['x'] + boxes['width'] / 2
        y_lower = boxes['y'] + boxes['height'] / 2

        cropped_image = input_image[int(y_upper):int(y_lower), int(x_upper):int(x_lower)]
        T, cropped_threshold_image = cv2.threshold(cropped_image, 236, 255,
                                                   cv2.THRESH_BINARY_INV)
        cropped_mask = cv2.cvtColor(cropped_threshold_image, cv2.COLOR_RGB2GRAY)
        input_image_width = int(model_output['image']['width'])
        input_mage_height = int(model_output['image']['height'])
        background = Image.fromarray(np.zeros(shape=(input_mage_height, input_image_width)))
        img_to_insert = Image.fromarray(cropped_mask)

        background.paste(img_to_insert, (int(x_upper), int(y_upper)))
        predicted_mask = np.array(background) / 255.0
        return predicted_mask

    async def _calculate_iou(self, generated_mask: Any, ground_truth_mask: Any) -> float:
        ground_truth_mask = cv2.cvtColor(cv2.imread(ground_truth_mask), cv2.COLOR_BGR2GRAY)
        ground_truth_mask = cv2.resize(ground_truth_mask, (generated_mask.shape[1], generated_mask.shape[0]))/255.0
        overlap = generated_mask * ground_truth_mask
        union = (generated_mask + ground_truth_mask) > 0
        iou = overlap.sum() / float(union.sum())
        return iou

    async def segment_furniture(self, request: schemas.InputPathsRequest) -> schemas.IoUResponse:
        images_paths = list(paths.list_images(request.input_images_folder_path))
        mask_paths = list(paths.list_images(request.input_masks_folder_path))
        logger.info(f"Количество входных изображений: {len(images_paths)}, количество масок: {len(mask_paths)}")
        mean_iou = 0
        for input_image_path, ground_truth_mask_path in zip(images_paths, mask_paths):
            logger.info(f"Обрабатывается изображение: {input_image_path} и маска: {ground_truth_mask_path}")
            segmented_image_info = await self.furniture_segmentation_gateway.segment_furniture(input_image_path)
            generated_mask = await self._process_model_output(segmented_image_info, input_image_path)
            iou = await self._calculate_iou(generated_mask, ground_truth_mask_path)
            logger.info(f"IoU of {input_image_path}: {iou}")
            mean_iou += iou

        response = await self._postprocess(mean_iou / len(list(paths.list_images(request.input_images_folder_path))))
        return response

    @staticmethod
    async def _postprocess(iou: float) -> schemas.IoUResponse:
        logger.info(f"IoU: {iou}")
        response = schemas.IoUResponse(iou=iou)

        return response
