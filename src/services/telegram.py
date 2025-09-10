from telethon.types import InputDocument
import config

from telethon import TelegramClient
from telethon.tl.functions.account import SaveMusicRequest


async def send_to_favorites(filename, caption=None):
    """Send a file to Telegram 'Saved Messages' (Favorites)."""
    async with TelegramClient("spotify_session", config.TELEGRAM_API_ID, config.TELEGRAM_API_HASH) as client:
        file = await client.send_file("me", filename, caption=caption)
        print(type(file))
        print(file)
        return file


async def add_to_profile(file_id: int, access_hash: int, file_reference: bytes):
    async with TelegramClient("spotify_session", config.TELEGRAM_API_ID, config.TELEGRAM_API_HASH) as client:
        result = await client(
            SaveMusicRequest(
                id=InputDocument(id=file_id, access_hash=access_hash, file_reference=file_reference),
                unsave=True
            )
        )
    return result
