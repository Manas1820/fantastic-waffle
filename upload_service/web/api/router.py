from fastapi.routing import APIRouter

from upload_service.web.api import monitoring
from upload_service.web.api import upload

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(upload.router)
