"""program entry point"""

from contextlib import asynccontextmanager

import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from loguru import logger

import routers


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    logger.info("Starting backend server")
    yield
    logger.info("Stopping backend server")


app = fastapi.FastAPI(lifespan=lifespan)

origins = [
    "*",
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.record.router, tags=["record"])


@app.get("/probes/healthiness")
def healthiness():
    return


if __name__ == "__main__":
    logger.info("Starting fastapi server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
