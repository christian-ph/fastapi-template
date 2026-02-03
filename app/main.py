from app.factory import create_app
from app.infrastructure.logging import logger
import uvicorn

app = create_app()

if __name__ == "__main__":
    logger.info("Starting application")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
