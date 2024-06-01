from datetime import date
from sqlalchemy import and_, or_, select, func, insert, delete
from typing import Any

from .models import Bookings
from app.hotels.models import Hotels
from app.users.models import Users
from ..hotels.rooms.models import Rooms
from ..dao.base import BaseDAO
from ..database import async_session_maker, engine


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def get_rooms_left(
            cls,
            room_id: int,
            date_from: date,
            date_to: date,
            session: Any
    ) -> int:
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        """
        booked_rooms = select(Bookings).where(
            and_(
                Bookings.room_id == room_id,
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    ),
                )
            )
        ).cte("booked_rooms")

        """
        # SELECT rooms.quantity - COUNT(booked_rooms.room_id)
        # FROM rooms
        # LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        # WHERE rooms.id = 1
        # GROUP_BY rooms.quantity, booked_rooms.room_id
        """
        get_rooms_left = select(
            (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
        ).select_from(Rooms).join(
            booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
        ).where(Rooms.id == room_id).group_by(
            Rooms.quantity, booked_rooms.c.room_id
        )
        # Вывести запрос в виде SQL
        # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

        rooms_left = await session.execute(get_rooms_left)
        return rooms_left.scalar()

    @classmethod
    async def get_user_bookings(cls, user_id: int):
        """
        SELECT bookings.*,
            rooms.image_id,
            rooms.name,
            rooms.description,
            rooms.services
        FROM bookings
        LEFT JOIN rooms ON bookings.room_id = rooms.id
        WHERE bookings.user_id = user_id
        """
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services
            ).join(
                Rooms, cls.model.room_id == Rooms.id, isouter=True
            ).where(cls.model.user_id == user_id)
            result = await session.execute(query)
            return result.mappings().all()
    
    @classmethod
    async def get_bookings_for_specific_data(cls, date: date):
        """
        SELECT bookings.*,
            hotels.name as hotel_name,
            users.email as user_email
        FROM bookings
        LEFT JOIN users ON bookings.user_id = users.id
        LEFT JOIN rooms ON bookings.room_id = rooms.id
        LEFT JOIN hotels ON rooms.hotel_id = hotels.id
        WHERE bookings.date_from = date
        """
        async with async_session_maker() as session:
            query = select(
                cls.model.__table__.columns,
                Hotels.name.label("hotel_name"),
                Users.email.label("user_email")
                ).select_from(
                    Bookings
                    ).join(
                        Users, cls.model.user_id == Users.id, isouter=True
                    ).join(
                        Rooms, cls.model.room_id == Rooms.id, isouter=True
                    ).join(
                        Hotels, Rooms.hotel_id == Hotels.id
                    ).where(cls.model.date_from == date)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls,
                  user_id: int,
                  room_id: int,
                  date_from: date,
                  date_to: date
                  ):
        async with async_session_maker() as session:
            rooms_left = await cls.get_rooms_left(room_id, date_from, date_to, session)
            if rooms_left > 0:
                query = select(Rooms.price).filter_by(id=room_id)
                room_price = await session.execute(query)
                room_price: int = room_price.scalar()
                add_booking = insert(Bookings).values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=room_price,

                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def delete(cls, booking_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == booking_id)
            await session.execute(query)
            await session.commit()
