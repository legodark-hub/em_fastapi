from fastapi import FastAPI
from api.routers.trade import router

app = FastAPI()

app.include_router(router, prefix="/api")