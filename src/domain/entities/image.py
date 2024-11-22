from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class ImageFrame:
    """
    Domain entity representing an image frame with its depth and pixel data.
    """

    depth: float
    pixel_data: np.ndarray
    id: Optional[int] = None

    @property
    def width(self) -> int:
        """Get the width of the image frame."""
        return self.pixel_data.shape[0]

    def resize(self, new_width: int) -> "ImageFrame":
        """
        Create a new ImageFrame with resized pixel data.

        Args:
            new_width (int): Target width for the resized image

        Returns:
            ImageFrame: New instance with resized data
        """
        resized_data = np.interp(
            np.linspace(0, self.width - 1, new_width),
            np.arange(self.width),
            self.pixel_data,
        )
        # img = Image.fromarray(self.pixel_data.reshape((1, self.width)))
        # img_resized = img.resize((1, new_width), Image.LANCZOS)
        # resized_data = np.array(img_resized).flatten()
        return ImageFrame(depth=self.depth, pixel_data=resized_data, id=self.id)
