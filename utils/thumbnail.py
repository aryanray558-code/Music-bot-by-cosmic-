import aiohttp
from PIL import Image, ImageDraw
from config import DOWNLOAD_PATH

async def generate_thumbnail(thumb_url: str, title: str):
    path = f"{DOWNLOAD_PATH}/thumb_{abs(hash(title))}.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(thumb_url) as resp:
            if resp.status == 200:
                with open(path, "wb") as f:
                    f.write(await resp.read())
    try:
        img = Image.open(path)
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), title[:40], fill=(255, 255, 255))
        img.save(path)
    except:
        pass
    return path
