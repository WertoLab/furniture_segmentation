
from fastapi import APIRouter, Depends

from app.core.furniture_segmentation_service import FurnitureSegmentationService
from app.core import schemas
from app.furniture_segmentation_service_container import get_furniture_segmentation_service

furniture_segmentation_router = APIRouter(
    prefix="/api/v1",
    tags=["Generate"],
    responses={404: {"description": "Not found"}},
)


@furniture_segmentation_router.post("/inference/", response_model=schemas.IoUResponse)
async def generate_sql_request(
        request: schemas.InputPathsRequest = None,
        service: FurnitureSegmentationService = Depends(get_furniture_segmentation_service)
):
    """
        ### Пример запроса:

        ```json
        {
            "input_images_folder_path": "/Users/andrey/Desktop/test_images",
            "input_masks_folder_path": "/Users/andrey/Desktop/test_masks"
        }
        ```

        ### Пример ответа:

        ```json
        {
            "iou": 0.62
        }
        ```
        """

    response = await service.segment_furniture(request)
    return response
