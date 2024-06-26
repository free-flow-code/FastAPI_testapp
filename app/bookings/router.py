from fastapi import APIRouter, Depends
from datetime import date
from pydantic import TypeAdapter

from app.tasks.tasks import send_booking_confirmation_email
from .dao import BookingDAO
from .schemas import SBooking
from ..users.models import Users
from ..users.dependendcies import get_current_user
from ..exeptions import RoomCannotBeBooked

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def fetch_user_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.get_user_bookings(user_id=user.id)


@router.post("")
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_adapter = TypeAdapter(SBooking)
    booking_dict = dict(booking_adapter.validate_python(booking))
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int):
    await BookingDAO.delete(booking_id)
