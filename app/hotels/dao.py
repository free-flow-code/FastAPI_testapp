from sqlalchemy import select, func
from datetime import date
from typing import Any

from ..database import async_session_maker
from ..dao.base import BaseDAO
from ..bookings.dao import BookingDAO
from .rooms.models import Rooms
from .models import Hotels


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotel_rooms_left(
            cls,
            room_ids: list,
            date_from: date,
            date_to: date,
            session: Any
    ) -> int:
        total_rooms_left = 0
        for room_id in room_ids:
            rooms_left = await BookingDAO.get_rooms_left(
                room_id=room_id,
                date_from=date_from,
                date_to=date_to,
                session=session
            )
            total_rooms_left += rooms_left
        return total_rooms_left

    @classmethod
    async def get_hotels_by_location(cls, location: str, date_from: date, date_to: date) -> list:
        """
        SELECT hotels.*,
            array_agg(rooms.id) AS room_ids
        FROM hotels
        JOIN rooms ON hotels.id = rooms.hotel_id
        WHERE hotels.location ILIKE '%location%'
        GROUP BY hotels.id;
        """
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns,
                (func.array_agg(Rooms.id)).label("room_ids")
            ).join(
                Rooms, cls.model.id == Rooms.hotel_id
            ).where(
                cls.model.location.ilike(f"%{location}%")
            ).group_by(cls.model.id)
            result = await session.execute(query)
            hotels = result.mappings().all()

            free_hotels = []
            for hotel in hotels:
                hotel_dict = dict(hotel)
                hotel_rooms_left = await cls.get_hotel_rooms_left(
                    hotel_dict.get("room_ids"),
                    date_from,
                    date_to,
                    session
                )

                if hotel_rooms_left > 0:
                    hotel_dict.update(rooms_left=hotel_rooms_left)
                    free_hotels.append(hotel_dict)

            return free_hotels
