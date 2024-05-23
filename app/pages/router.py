from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from ..hotels.router import fetch_hotels_by_location

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def find_hotels_page(
        request: Request,
        hotels=Depends(fetch_hotels_by_location)
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels},
    )
