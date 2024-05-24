import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .bookings.router import router as router_bookings
from .users.router import router as router_users
from .hotels.router import router as router_hotels
from .hotels.rooms.router import router as router_rooms
from .pages.router import router as router_pages
from .images.router import router as router_images

logging.basicConfig(
        level=logging.DEBUG,
        filename='py_log.log',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s'
    )

app = FastAPI(title="Бронирования отелей")

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)

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
