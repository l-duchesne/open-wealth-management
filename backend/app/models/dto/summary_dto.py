from enum import Enum

from pydantic import BaseModel, ConfigDict


class WeathTypeDtoSchema(Enum):
    STOCK_MARKET = "stock_market"
    REAL_ESTATE_ACTIVE = "real_estate_active"
    REAL_ESTATE_PASSIVE = "real_estate_passive"
    SAVINGS = "savings"
    CRYPTO_CURRENCY = "crypto_currency"
    CURRENCY = "currency"


class SummaryDetailDtoSchema(BaseModel):
    type: WeathTypeDtoSchema
    value: float
    model_config = ConfigDict(from_attributes=True)


class SummaryDtoSchema(BaseModel):
    grossSum: float
    netSum: float
    details: list[SummaryDetailDtoSchema]
    model_config = ConfigDict(from_attributes=True)
