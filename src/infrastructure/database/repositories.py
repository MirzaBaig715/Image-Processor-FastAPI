from typing import List, Optional

import numpy as np
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.image import ImageFrame
from src.domain.interfaces.repositories import ImageRepository
from src.infrastructure.database.models import ImageModel


class SQLAlchemyImageRepository(ImageRepository):
    """Implementation of ImageRepository using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_save(self, frames: List[ImageFrame]) -> None:
        """
        Save an image frame to the database.

        Args:
            frames: List of ImageFrame to bulk save for large data population
        """
        models = [
            ImageModel(depth=image.depth, pixel_data=image.pixel_data.tobytes())
            for image in frames
        ]
        self.session.add_all(models)
        await self.session.commit()

    async def save(self, image: ImageFrame) -> ImageFrame:
        """
        Save an image frame to the database.

        Args:
            image: ImageFrame to save

        Returns:
            ImageFrame: Saved image with updated ID
        """
        model = ImageModel(depth=image.depth, pixel_data=image.pixel_data.tobytes())
        self.session.add(model)
        await self.session.commit()

        return ImageFrame(
            id=model.id,
            depth=model.depth,
            pixel_data=np.frombuffer(model.pixel_data, dtype=np.uint8),
        )

    async def get_by_depth_range(
        self, depth_min: float, depth_max: float
    ) -> List[ImageFrame]:
        """
        Retrieve image frames within the specified depth range.

        Args:
            depth_min: Minimum depth value
            depth_max: Maximum depth value

        Returns:
            List[ImageFrame]: List of matching image frames
        """
        query = (
            select(ImageModel)
            .where(and_(ImageModel.depth >= depth_min, ImageModel.depth <= depth_max))
            .order_by(ImageModel.depth)
        )

        result = await self.session.execute(query)
        models = result.scalars().all()

        return [
            ImageFrame(
                id=model.id,
                depth=model.depth,
                pixel_data=np.frombuffer(model.pixel_data, dtype=np.float64),
            )
            for model in models
        ]

    async def get_by_id(self, _id: int) -> Optional[ImageFrame]:
        """
        Retrieve an image frame by its ID.

        Args:
            _id: Image frame ID

        Returns:
            Optional[ImageFrame]: Matching image frame or None
        """
        query = select(ImageModel).filter(ImageModel.id == _id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return ImageFrame(
            id=model.id,
            depth=model.depth,
            pixel_data=np.frombuffer(model.pixel_data, dtype=np.float64),
        )
