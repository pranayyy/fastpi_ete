from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, declarative_base
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
import time
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/blogdb")

def create_database_engine(max_retries=30, retry_delay=2):
    """Create database engine with retry logic"""
    for attempt in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
            return engine
        except OperationalError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Failed to connect to database after {max_retries} attempts")
                raise

engine = create_database_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()
