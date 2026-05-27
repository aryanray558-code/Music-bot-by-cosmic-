from database.mongo import queues
from bot import call_py
from py_tgcalls.types.input_stream import AudioPiped
from py_tgcalls.types.input_stream.quality import HighQualityAudio
from py_tgcalls.types import StreamType

async def get_queue(chat_id):
    data = await queues.find_one({"chat_id": chat_id})
    return data or {"chat_id": chat_id, "queue": []}

async def add_to_queue(chat_id, track):
    queue_data = await get_queue(chat_id)
    queue_data["queue"].append(track)
    await queues.update_one({"chat_id": chat_id}, {"$set": queue_data}, upsert=True)

async def start_stream(chat_id):
    queue_data = await get_queue(chat_id)
    if not queue_data["queue"]:
        return
    track = queue_data["queue"][0]
    try:
        await call_py.join_group_call(
            chat_id,
            AudioPiped(track["file"], HighQualityAudio()),
            stream_type=StreamType().local_stream
        )
    except Exception as e:
        print(f"Stream Error: {e}")
