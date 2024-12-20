from typing import Optional

from pydantic import BaseModel, ConfigDict


class ItemDtoSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool

    model_config = ConfigDict(from_attributes=True)
