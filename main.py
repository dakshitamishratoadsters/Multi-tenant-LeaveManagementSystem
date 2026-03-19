from fastapi import FastAPI
from src.api.v1.router.routes import api_router

app = FastAPI()

app.include_router(api_router)