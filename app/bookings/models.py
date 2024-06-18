from sqlalchemy import Integer, Column, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship
from ..database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, nullable=False)
    room_id = Column(ForeignKey("rooms.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_from - date_to) * price"))
    total_days = Column(Integer, Computed("date_from - date_to"))

    user = relationship("Users", back_populates="booking")
    room = relationship("Rooms", back_populates="booking")

    def __str__(self):
        return f"Бронь #{self.id}"
