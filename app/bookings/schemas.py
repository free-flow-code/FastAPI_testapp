from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional


class SBooking(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    services: Optional[list]
