from app.models.db.database import get_db
from app.services import refresh_service
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/refresh", tags=["refresh"])


@router.post("/", response_model=str)
async def refresh(db: AsyncSession = Depends(get_db)):
    await refresh_service.refresh(db)
    return ""
