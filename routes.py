from fastapi import APIRouter
from line_routes import line_router

router = APIRouter()

router.include_router(line_router, prefix="/api")
