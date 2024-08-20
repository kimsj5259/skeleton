import sys
import logging

from fastapi import FastAPI, Request
from loguru import logger

from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from .apps.router import api_router
from .core.config import settings

app = FastAPI()


# TODO: 어떤 로깅이 좋을지는 보면서 판단
# CustomizeLogger.customize_logging(level)
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{level}</green> <yellow>{name}</yellow> {message}", level=level)
logging.basicConfig(level=logging.INFO)

async def log_request_middleware(request: Request, call_next):
    if request.url.path[-1] != '/':
        logger.info(f"Received request: {request.method} {request.url}")
    
    response = await call_next(request)
    if request.url.path[-1] != '/':
        logger.info(f"Sent response: {response.status_code}")

    return response

# 미들웨어 등록
app.middleware("http")(log_request_middleware)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.ASYNC_DATABASE_URI,
    engine_args={
        "echo": True,
        "pool_pre_ping": True,
        "pool_size": settings.POOL_SIZE,
        "max_overflow": 64,
    },
)

@app.get("/")
async def health_check():
    return {"status": "OK"}

app.include_router(api_router, prefix="/API_v1")