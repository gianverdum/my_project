import logging

from fastapi import FastAPI

from src.my_project.database.database import engine, init_db
from src.my_project.routers.members import router as members_router

# Configure logging to record application events
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a FastAPI instance
app = FastAPI()

# Include the members router
app.include_router(members_router)

# Initialize the database and log the status
try:
    init_db(engine)
    logger.info("Database initialized and tables created.")
except Exception as e:
    logger.error(f"Error initializing the database: {e}")


# Define the root endpoint
@app.get("/", response_model=dict)
def read_root() -> dict:
    return {"message": "Welcome to the Rotary Club API!"}
