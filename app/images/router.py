from fastapi import APIRouter, UploadFile
import aiofiles

router = APIRouter(
    prefix="/images",
    tags=["Загрузка изображений"]
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    async with aiofiles.open(f"app/static/images/{name}.webp", "wb+") as file_object:
        while True:
            content = await file.read(1024)
            if not content:
                break
            await file_object.write(content)
