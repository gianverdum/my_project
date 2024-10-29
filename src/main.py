from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.database import engine
from src.models.member import Base
from src.routers.member_router import router as member_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

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
    return {"status": "OK"}


# Root endpoint
@app.get("/", summary="Root endpoint", response_description="Welcome message")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the members API!"}


# Include routers
app.include_router(member_router, prefix="/api", tags=["members"])


# Global exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
