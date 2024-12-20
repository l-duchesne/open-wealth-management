from app.models.dto.summary_dto import SummaryDtoSchema
from app.services import summary_service
from fastapi import APIRouter

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/", response_model=SummaryDtoSchema)
async def get_summary():
    return summary_service.get_summary()
