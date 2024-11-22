import math
from typing import List, Literal, Union

import numpy as np
from pydantic import BaseModel, Field

# Color mapping list
COLOR_MAPS = [
    "magma",
    "inferno",
    "plasma",
    "viridis",
    "cividis",
    "twilight",
    "twilight_shifted",
    "turbo",
    "Blues",
    "BrBG",
    "BuGn",
]


def safe_float_encoder(x):
    """
    Check for NaN or infinity values and replace with null
    """
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return None
    return x


class NumpyArrayModel(BaseModel):
    """Model to handle numpy array serialization."""

    data: List[List[Union[int, float]]] = Field(..., description="list of RGB values")

    @classmethod
    def from_numpy(cls, array: np.ndarray) -> "NumpyArrayModel":
        return cls(data=array.tolist())

    def to_numpy(self) -> np.ndarray:
        return np.array(self.data)


class ImageResponse(BaseModel):
    """Response schema for image frames data."""

    id: int
    depth: float
    pixels: NumpyArrayModel

    @classmethod
    def from_raw_data(
        cls, _id: int, depth: float, pixels: np.ndarray
    ) -> "ImageResponse":
        """Prepare response data."""
        return cls(
            id=_id,
            depth=safe_float_encoder(depth),
            pixels=NumpyArrayModel.from_numpy(pixels),
        )


class DepthRangeRequest(BaseModel):
    """Request schema for depth range queries."""

    depth_min: float = Field(..., description="Minimum depth value")
    depth_max: float = Field(..., description="Maximum depth value")
    color_map: Literal[*COLOR_MAPS] = Field(
        ..., description="Color mapping value", examples=COLOR_MAPS
    )
