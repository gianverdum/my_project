# main.py
from fastapi import FastAPI
from .routers.members import router as members_router
from .database.database import init_db, engine  # Import the engine
import logging

# Configure logging to record application events
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a FastAPI instance
app = FastAPI()

# Include the members router
app.include_router(members_router)

# Initialize the database and log the status
try:
    init_db(engine)  # Pass the engine to initialize the database
    logger.info("Database initialized and tables created.")  # Log success message
except Exception as e:
    logger.error(f"Error initializing the database: {e}")  # Log any errors encountered

# Define the root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Rotary Club API!"}  # Return welcome message
