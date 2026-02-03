from pytgcalls.types import Update, StreamAudioEnded

from . import queues
from ..clients.clients import call
from .streams import run_stream, close_stream


async def run_async_calls():

    @call.on_update()
    async def stream_handler(_, update: Update):

        # When current audio stream ends
        if isinstance(update, StreamAudioEnded):
            chat_id = update.chat_id
            queues.task_done(chat_id)

            if queues.is_empty(chat_id):
                return await close_stream(chat_id)

            data = queues.get(chat_id)
            file = data["file"]
            stream_type = data["type"]

            stream = await run_stream(file, stream_type)
            return await call.play(chat_id, stream)