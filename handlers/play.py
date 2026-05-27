from pyrogram import filters
from pyrogram.types import Message
from bot import bot
from utils.downloader import download_media
from utils.thumbnail import generate_thumbnail
from handlers.queue import add_to_queue, start_stream
from database.mongo import queues

@bot.on_message(filters.command("play") & filters.group)
async def play_command(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**Usage:** `/play <song name or link>`")
    
    query = " ".join(message.command[1:])
    msg = await message.reply_text("🔍 **Searching & Downloading...**")

    try:
        file_path, title, thumb_url = await download_media(query)
        thumb = await generate_thumbnail(thumb_url, title) if thumb_url else None

        await add_to_queue(message.chat.id, {
            "file": file_path,
            "title": title,
            "thumb": thumb
        })

        queue_data = await get_queue(message.chat.id)
        if len(queue_data["queue"]) == 1:
            await start_stream(message.chat.id)

        await msg.edit_text(f"✅ **Queued:** {title}")
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)[:700]}")
