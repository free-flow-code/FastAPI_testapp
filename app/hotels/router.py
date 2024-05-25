from fastapi import APIRouter
from datetime import date
from typing import Optional
from fastapi_cache.decorator import cache

from .schemas import SHotel
from .dao import HotelDAO

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("")
@cache(expire=30)
async def get_hotels() -> list[SHotel]:
    return await HotelDAO.find_all()


@router.get("/{location}")
@cache(expire=30)
async def fetch_hotels_by_location(
        location: str,
        date_from: date,
        date_to: date
) -> list[SHotel]:
    return await HotelDAO.get_hotels_by_location(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SHotel]:
    return await HotelDAO.find_one_or_none(id=hotel_id)
