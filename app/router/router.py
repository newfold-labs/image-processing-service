from fastapi import APIRouter, Depends
from app.services import ApiTokenAuthService
from .trim_route import trim_route

# '/image' route
router = APIRouter(
    prefix="/image",
    tags=["image"],
    dependencies=[Depends(ApiTokenAuthService.verify_token)]
)

# Include trim route '/image/trim'
router.include_router(trim_route) 