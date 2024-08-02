from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumer import make_broker_connection
from app.event.handlers import router as event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_broker_connection()
    yield

app = FastAPI(title='event_broker', lifespan=lifespan)

app.include_router(event_router)
