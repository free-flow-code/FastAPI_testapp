import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from contextlib import asynccontextmanager

from .config import settings
from .bookings.router import router as router_bookings
from .users.router import router as router_users
from .hotels.router import router as router_hotels
from .hotels.rooms.router import router as router_rooms
from .pages.router import router as router_pages
from .images.router import router as router_images
from .admin.views import UsersAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin
from .database import engine
from .admin.auth import authentication_backend

logging.basicConfig(
        level=logging.DEBUG,
        filename='py_log.log',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s'
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Service started")
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
        )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    logging.info("Service exited")

app = FastAPI(
    title="Бронирования отелей",
    lifespan=lifespan,
    )
admin = Admin(app, engine, authentication_backend=authentication_backend)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

origins = settings.ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization"],
)
