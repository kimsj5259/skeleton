from fastapi import FastAPI
from .apps.router import api_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix="/API_v1")