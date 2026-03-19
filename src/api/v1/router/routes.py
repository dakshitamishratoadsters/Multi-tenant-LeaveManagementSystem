from fastapi import APIRouter
from src.api.v1.endpoints.user_endpoints import router as user_router

api_router = APIRouter()

api_router.include_router(user_router)
# include tenant routes
api_router.include_router(tenant_endpoints.router)
