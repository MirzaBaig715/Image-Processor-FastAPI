from sqlalchemy import Column, Float, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ImageModel(Base):
    """SQLAlchemy model for storing image frames."""

    __tablename__ = "image_frames"

    id = Column(Integer, primary_key=True)
    depth = Column(Float, index=True, nullable=False)
    pixel_data = Column(LargeBinary, nullable=False)
