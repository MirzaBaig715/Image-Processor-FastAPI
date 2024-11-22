from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import DepthRangeRequest, ImageResponse
from src.config.database import get_session
from src.core.exceptions import AppException, NotFoundError
from src.domain.services.color_map import CustomColorMap
from src.infrastructure.database.repositories import SQLAlchemyImageRepository

router = APIRouter()


@router.post("/frames/by-depth", response_model=List[ImageResponse])
async def get_image_frames_by_depth(
    request: DepthRangeRequest, session: AsyncSession = Depends(get_session)
):
    """
    Retrieve and color-map frames within the specified depth range.

    Args:
        request: Depth range and color map parameters
        session: Database session

    Returns:
        List[ImageResponse]: List of processed image frames
    """
    repository = SQLAlchemyImageRepository(session)
    frames = await repository.get_by_depth_range(request.depth_min, request.depth_max)

    if not frames:
        raise NotFoundError(detail="No frames found in this depth range")
    try:
        color_mapper = CustomColorMap(request.color_map)
        processed_frames = [
            ImageResponse.from_raw_data(
                _id=frame.id,
                depth=frame.depth,
                pixels=color_mapper.apply(frame.pixel_data),
            )
            for frame in frames
        ]
    except Exception:
        raise AppException(status_code=400)

    return processed_frames


@router.get("/frames/{frame_id}", response_model=ImageResponse)
async def get_image_frames_by_id(
    frame_id: int, session: AsyncSession = Depends(get_session)
):
    """
    Retrieve and color-map frames within the specified depth range.

    Args:
        frame_id: Frame ID
        session: Database session

    Returns:
        ImageResponse: Processed image frame with custom color map.
    """
    repository = SQLAlchemyImageRepository(session)
    frame = await repository.get_by_id(frame_id)

    if not frame:
        raise NotFoundError(detail="No frame found for specified ID")
    try:
        color_mapper = CustomColorMap()
        frame = ImageResponse.from_raw_data(
            _id=frame.id, depth=frame.depth, pixels=color_mapper.apply(frame.pixel_data)
        )
        return frame
    except Exception:
        raise AppException(status_code=400)
