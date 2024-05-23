from pydantic import BaseModel, ConfigDict
from typing import Optional


class SHotel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int
    rooms_left: Optional[int] = None
