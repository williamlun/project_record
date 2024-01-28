"""program entry point"""

import fastapi
import uvicorn
import routers
from loguru import logger


app = fastapi.FastAPI()


if __name__ == "__main__":
    logger.info("Starting backend server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
