from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumer import make_broker_consumer
from app.bets.handlers import router as bets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await make_broker_consumer()
    yield

app = FastAPI(title='bet-maker', lifespan=lifespan)
app.include_router(bets_router)
