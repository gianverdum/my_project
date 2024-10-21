from fastapi import FastAPI
from src.my_project.routers.members import router as members_router

app = FastAPI()

# Include the members router
app.include_router(members_router)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
