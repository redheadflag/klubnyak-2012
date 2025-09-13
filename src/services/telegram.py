from functools import partial
import time
from telethon.types import InputDocument
from telethon.tl.types.account import SavedMusicIds

from telethon import TelegramClient
from telethon.tl.functions.account import SaveMusicRequest, GetSavedMusicIdsRequest

from config import telegram_config
from schemas import DownloadedSong, UploadedSong


client = TelegramClient("spotify_session", telegram_config.api_id, telegram_config.api_hash)


async def send_to_favorites(downloaded_song: DownloadedSong) -> UploadedSong:
    """Send a file to Telegram 'Saved Messages' (Favorites)."""
    file = await client.send_file("me", str(downloaded_song.path))

    if not (document := getattr(file, "document", None)):
        raise ValueError("Telegram did not return a document for uploaded file.")
    
    return UploadedSong(
        title=downloaded_song.title,
        artist=downloaded_song.artist,
        duration_sec=downloaded_song.duration_sec,
        file_id=document.id,
        access_hash=document.access_hash,
        file_reference=document.file_reference
    )


async def _save_music(uploaded_song: UploadedSong, unsave: bool):
    result = await client(
        SaveMusicRequest(
            id=InputDocument(
                id=uploaded_song.file_id,
                access_hash=uploaded_song.access_hash,
                file_reference=uploaded_song.file_reference
            ),
            unsave=unsave
        )
    )
    if unsave:
        print(f"Song {str(uploaded_song)} was removed from profile")
    else:
        print(f"Song {str(uploaded_song)} was added to profile")
    return result


add_to_profile = partial(_save_music, unsave=False)
remove_from_profile = partial(_save_music, unsave=True)


async def get_saved_music_ids() -> SavedMusicIds:
    result = await client(
        GetSavedMusicIdsRequest(
            hash=int(time.time())
        )
    )
    return result
