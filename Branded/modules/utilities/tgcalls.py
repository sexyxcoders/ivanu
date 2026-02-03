from pytgcalls.types import (
    Update,
    ChatUpdate,
    ChatUpdateStatus,
    StreamAudioEnded,
)

from . import queues
from ..clients.clients import app, call
from .streams import run_stream, close_stream


async def run_async_calls():

    @call.on_update()
    async def stream_services_handler(_, update: Update):

        # VC closed / kicked / left
        if isinstance(update, ChatUpdate):
            if update.status in (
                ChatUpdateStatus.CLOSED_VOICE_CHAT,
                ChatUpdateStatus.KICKED,
                ChatUpdateStatus.LEFT_GROUP,
            ):
                return await close_stream(update.chat_id)

        # Audio stream ended
        if isinstance(update, StreamAudioEnded):
            chat_id = update.chat_id
            queues.task_done(chat_id)

            if queues.is_empty(chat_id):
                return await close_stream(chat_id)

            check = queues.get(chat_id)
            file = check["file"]
            stream_type = check["type"]

            stream = await run_stream(file, stream_type)
            return await call.play(chat_id, stream)