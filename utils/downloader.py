import asyncio
import yt_dlp
from config import DOWNLOAD_PATH

async def download_media(query: str):
    loop = asyncio.get_event_loop()
    def run_ydl():
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_PATH}/%(id)s.%(ext)s',
            'quiet': True,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query if query.startswith("http") else f"ytsearch:{query}", download=True)
            if 'entries' in info:
                info = info['entries'][0]
            return ydl.prepare_filename(info), info.get('title'), info.get('thumbnail')
    return await loop.run_in_executor(None, run_ydl)
