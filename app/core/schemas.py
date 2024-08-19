from pydantic import BaseModel


class InputPathsRequest(BaseModel):
    input_images_folder_path: str
    input_masks_folder_path: str


class IoUResponse(BaseModel):
    iou: float
