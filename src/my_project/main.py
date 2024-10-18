from fastapi import FastAPI
from .database import init_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize database
try:
    init_db()
    logger.info("Database initialized and tables created.")
except Exception as e:
    logger.error(f"Error initializing the database: {e}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Rotary Club API!"}
