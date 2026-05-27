from pyrogram import filters
from pyrogram.types import Message
from bot import bot, call_py
from handlers.queue import start_stream
from database.mongo import queues

@bot.on_message(filters.command(["pause", "resume", "skip", "clear"]) & filters.group)
async def controls(_, message: Message):
    cmd = message.command[0].lower()
    chat_id = message.chat.id

    if cmd == "pause":
        await call_py.pause_stream(chat_id)
        await message.reply_text("⏸ **Paused**")
    elif cmd == "resume":
        await call_py.resume_stream(chat_id)
        await message.reply_text("▶️ **Resumed**")
    elif cmd == "skip":
        await call_py.leave_group_call(chat_id)
        await start_stream(chat_id)
        await message.reply_text("⏭ **Skipped**")
    elif cmd == "clear":
        await queues.delete_one({"chat_id": chat_id})
        await call_py.leave_group_call(chat_id)
        await message.reply_text("🗑 **Queue Cleared**")
