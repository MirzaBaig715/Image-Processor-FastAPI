from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np


class ColorMap(ABC):
    @abstractmethod
    def apply(self, pixel_data: np.ndarray) -> np.ndarray:
        pass


class CustomColorMap(ColorMap):
    """Implementation of color mapping."""

    def __init__(self, color_map="viridis"):
        """
        Initialize with color mapping.
        """
        self.color_map = plt.cm.get_cmap(color_map)

    def apply(self, pixel_data: np.ndarray) -> np.ndarray:
        """
        Apply color mapping to normalized pixel data.

        Args:
            pixel_data: Input grayscale image data (0-255)

        Returns:
            np.ndarray: RGB color-mapped image data
        """
        # Normalize input data to 0-1 range for matplot
        normalized = pixel_data.astype(float) / 255.0
        colored_pixels = self.color_map(normalized)
        # Convert RGBA to RGB uint8. Easier to use uint8 type data for general processing
        rgb_pixels = (colored_pixels[:, :3] * 255).astype(np.uint8)
        return rgb_pixels
