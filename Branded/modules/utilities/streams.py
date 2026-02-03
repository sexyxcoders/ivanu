import os
import yt_dlp

from asyncio.queues import QueueEmpty
from youtubesearchpython.__future__ import VideosSearch

from pytgcalls.types.input_stream import AudioPiped, VideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
)

from . import queues
from ..clients.clients import call
from ...console import USERBOT_PICTURE


# -------------------- YouTube Search --------------------

async def get_result(query: str):
    results = VideosSearch(query, limit=1)
    for result in (await results.next())["result"]:
        url = result["link"]
        try:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        except:
            thumbnail = USERBOT_PICTURE

    return url, thumbnail


# -------------------- Stream Builder --------------------

async def run_stream(source, stream_type):
    """
    source: local file path OR direct URL
    stream_type: 'Audio' | 'Video'
    """

    if stream_type == "Video":
        return VideoPiped(
            source,
            HighQualityVideo(),
            HighQualityAudio(),
        )

    # Default: Audio
    return AudioPiped(
        source,
        HighQualityAudio(),
    )


# -------------------- Cleanup --------------------

async def close_stream(chat_id):
    try:
        await queues.clear(chat_id)
    except QueueEmpty:
        pass

    try:
        await call.leave_group_call(chat_id)
    except:
        pass