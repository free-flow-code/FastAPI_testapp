from pydantic import BaseModel, ConfigDict
from typing import Optional


class SRoom(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int
    rooms_left: Optional[int]
    total_cost: Optional[int]
