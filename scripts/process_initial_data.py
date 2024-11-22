"""
Script to process the initial CSV data file and populate the database.
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from src.config.database import async_session
from src.core.log_handlers import setup_logging
from src.infrastructure.database.repositories import SQLAlchemyImageRepository
from src.infrastructure.services.image_processor import ImageProcessor


async def process_csv_file():
    """Process the CSV file and store images in the database."""
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting CSV processing")

        csv_path = Path(__file__).parent.parent / "data" / "img.csv"
        frames = await ImageProcessor.process_csv(str(csv_path))

        logger.info(f"Processed {len(frames)} frames from CSV")

        # Store in database
        async with async_session() as session:
            repository = SQLAlchemyImageRepository(session)
            await repository.bulk_save(frames)

        logger.info("CSV processing completed successfully")

    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}")
        raise

    finally:
        # Loop through all handlers and close them
        for handler in logger.handlers:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    asyncio.run(process_csv_file())
