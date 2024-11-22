from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.image import ImageFrame


class ImageRepository(ABC):
    """Abstract base class defining the interface for image storage."""

    @abstractmethod
    async def save(self, image: ImageFrame) -> ImageFrame:
        """Save an image frame to the storage."""
        pass

    @abstractmethod
    async def get_by_depth_range(
        self, depth_min: float, depth_max: float
    ) -> List[ImageFrame]:
        """Retrieve image frames within the specified depth range."""
        pass

    @abstractmethod
    async def get_by_id(self, _id: int) -> Optional[ImageFrame]:
        """Retrieve an image frame by its ID."""
        pass
