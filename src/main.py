# src/main.py
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.database import engine  # Using `engine` from `src/database.py`
from src.models.member import Base
from src.routers.member_router import router as member_router

# Load environment variables from .env file
load_dotenv()

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My Project API",
    description="This API allows managing members.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Members",
            "description": "Operations with members.",
        },
    ],
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
def health_check() -> dict[str, str]:
    """
    Checks the API's health status.

    Returns:
        dict[str, str]: A JSON object indicating the API is operational.
    """
    return {"status": "OK"}


# Root endpoint
@app.get("/", summary="Root endpoint", response_description="Welcome message")
def read_root() -> dict[str, str]:
    """
    Root endpoint providing a welcome message.

    Returns:
        dict[str, str]: A JSON welcome message.
    """
    return {"message": "Welcome to the members API!"}


# Include routers
app.include_router(member_router, prefix="/api", tags=["members"])


# Global exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handles HTTP exceptions across the application,\
        returning a JSON error response.

    Args:
        request (Request): The incoming request.
        exc (HTTPException): The HTTP exception raised.

    Returns:
        JSONResponse: JSON response with error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
