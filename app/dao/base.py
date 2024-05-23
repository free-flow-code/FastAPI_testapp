from sqlalchemy import select, insert

from ..database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            # __table__.columns нужен для отсутствия вложенности в ответе Алхимии
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().first()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            # __table__.columns нужен для отсутствия вложенности в ответе Алхимии
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().first()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            # __table__.columns нужен для отсутствия вложенности в ответе Алхимии
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
