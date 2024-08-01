from fastapi import FastAPI

from app.event.handlers import router as event_router

app = FastAPI(title='event_broker')

app.include_router(event_router)
