from fastapi import APIRouter
from app.infrastructure.logging import logger

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    logger.debug("Health check called")
    return {"status": "ok"}
