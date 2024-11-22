from typing import List

import pandas as pd

from src.domain.entities.image import ImageFrame


class ImageProcessor:
    """Service for processing image data from CSV files."""

    @staticmethod
    async def process_csv(file_path: str, target_width: int = 150) -> List[ImageFrame]:
        """
        Process CSV file containing image data and create ImageFrame objects.

        Args:
            file_path: Path to the CSV file
            target_width: Desired width for the processed images

        Returns:
            List[ImageFrame]: List of processed image frames
        """
        # Read CSV file
        df = pd.read_csv(file_path)

        # Extract depth values and pixel data
        depths = df["depth"].values
        pixel_data = df.drop("depth", axis=1).values

        # Create ImageFrame objects
        frames = []
        for depth, pixels in zip(depths, pixel_data):
            frame = ImageFrame(depth=depth, pixel_data=pixels)
            if target_width != frame.width:
                frame = frame.resize(target_width)
            frames.append(frame)

        return frames
