from functools import partial
import time
from telethon.types import InputDocument
from config import telegram_config

from telethon import TelegramClient
from telethon.tl.functions.account import SaveMusicRequest, GetSavedMusicIdsRequest


client = TelegramClient("spotify_session", telegram_config.api_id, telegram_config.api_hash)


async def send_to_favorites(filename):
    """Send a file to Telegram 'Saved Messages' (Favorites)."""
    file = await client.send_file("me", filename)
    return file


async def _save_music(file_id: int, access_hash: int, file_reference: bytes, unsave: bool):
    result = await client(
        SaveMusicRequest(
            id=InputDocument(id=file_id, access_hash=access_hash, file_reference=file_reference),
            unsave=unsave
        )
    )
    return result


add_to_profile = partial(_save_music, unsave=False)
remove_from_profile = partial(_save_music, unsave=True)


async def get_saved_music_ids():
    result = await client(
        GetSavedMusicIdsRequest(
            hash=int(time.time())
        )
    )
    return result
