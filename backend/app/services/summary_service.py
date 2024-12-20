from app.models.dto.summary_dto import SummaryDtoSchema,SummaryDetailDtoSchema, WeathTypeDtoSchema


def get_summary():
    return SummaryDtoSchema(grossSum = 10, netSum =1524, details= [ SummaryDetailDtoSchema(type = WeathTypeDtoSchema.CURRENCY, value=1245)])