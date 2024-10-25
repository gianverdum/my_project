# src/main.py
from fastapi import FastAPI

from src.routers.member_router import router as member_router

app = FastAPI()

app.include_router(member_router, prefix="/api", tags=["members"])


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to the members API!"}
