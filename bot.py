import asyncio
from pyrogram import Client
from py_tgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client("PremiumMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(bot)

# Import all handlers
import handlers.play
import handlers.controls

async def main():
    await bot.start()
    await call_py.start()
    print("🚀 Premium VC Music Bot Started Successfully!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
