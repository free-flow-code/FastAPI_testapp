from fastapi import APIRouter, UploadFile
import aiofiles

from app.tasks.tasks import process_image

router = APIRouter(
    prefix="/images",
    tags=["Загрузка изображений"]
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    image_path = f"app/static/images/{name}.webp"
    async with aiofiles.open(image_path, "wb+") as file_object:
        while True:
            content = await file.read(1024)
            if not content:
                break
            await file_object.write(content)
    process_image.delay(image_path)
