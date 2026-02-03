from ..clients.clients import call
from . import queues
from .streams import run_stream, close_stream


async def run_async_calls():

    @call.on_stream_end()
    async def stream_end_handler(_, chat_id: int):
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            return await close_stream(chat_id)

        data = queues.get(chat_id)
        file = data["file"]
        stream_type = data["type"]

        stream = await run_stream(file, stream_type)
        return await call.play(chat_id, stream)