from fastapi import APIRouter

from app.auth import profile
from app.auth import admin

router = APIRouter()

router.include_router(profile.router)
router.include_router(admin.router)