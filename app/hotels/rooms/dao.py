from sqlalchemy import select
from datetime import date
from typing import Any

from .models import Rooms
from ..models import Hotels
from ...bookings.dao import BookingDAO
from ...dao.base import BaseDAO
from ...database import async_session_maker


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_hotel_rooms_id(cls, hotel_id: int, session: Any) -> list:
        query = select(RoomsDAO.model.__table__.columns).filter_by(hotel_id=hotel_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_hotel_rooms(cls, hotel_id: int, date_from: date, date_to: date) -> list:
        async with async_session_maker() as session:
            """
            # SELECT rooms.*,
	        #    ((days_to - days_from).days * rooms.price) as total_cost
            # FROM rooms
            # LEFT JOIN hotels ON rooms.hotel_id = hotels.id
            # WHERE rooms.hotel_id = hotel_id
            """
            query = select(
                cls.model.__table__.columns,
                ((date_to - date_from).days * cls.model.price).label("total_cost")
            ).join(
                Hotels, cls.model.hotel_id == Hotels.id, isouter=True
            ).where(cls.model.hotel_id == hotel_id)
            result = await session.execute(query)
            rooms = result.mappings().all()

            rooms_data = []
            for room in rooms:
                room_dict = dict(room)
                rooms_left = await BookingDAO.get_rooms_left(
                    room_id=room_dict.get("id"),
                    date_from=date_from,
                    date_to=date_to,
                    session=session
                )
                room_dict.update(rooms_left=rooms_left)
                rooms_data.append(room_dict)

            return rooms_data
