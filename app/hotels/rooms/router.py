from datetime import date

from .dao import RoomsDAO
from .schemas import SRoom
from ..router import router


@router.get("/{hotel_id}/room")
async def fetch_hotel_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRoom]:
    return await RoomsDAO.get_hotel_rooms(hotel_id, date_from, date_to)
