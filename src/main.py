import asyncio

from config import (
    spotify_config,
    general_config,
    telegram_config
)
from schemas import Memory
from services import (
    spotify,
    telegram,
    youtube
)


memory = Memory()


async def polling_currently_playing() -> None:
    try:
        while True:
            song = spotify.get_current_track()    
            if not song:
                print("No song")
                await asyncio.sleep(spotify_config.refresh_time)
                continue
            if memory.is_same_song(song):
                print(f"The same song is playing. Sleep for {spotify_config.refresh_time}s")
                await asyncio.sleep(spotify_config.refresh_time)
                continue
            try:
                downloaded_song = youtube.search_and_download(song=song)
            except ValueError:
                print(f"Song not found. Sleep for {song.duration_sec}s")
                await asyncio.sleep(song.duration_sec)
                continue
            
            file = await telegram.send_to_favorites(filename=downloaded_song.path)
            await telegram.add_to_profile(file.document.id, file.document.access_hash, file.document.file_reference)
            
            await asyncio.sleep(1)

            if memory.file:
                await telegram.remove_from_profile(
                    memory.file.document.id,
                    memory.file.document.access_hash,
                    memory.file.document.file_reference
                )
            if general_config.remove_downloads:
                downloaded_song.path.unlink(missing_ok=True)

            memory.song = song
            memory.file = file

            await asyncio.sleep(spotify_config.refresh_time)

    except asyncio.CancelledError:
        print("Polling has been stopped")


async def main():
    await telegram.client.start(
        phone=telegram_config.phone,
        password=telegram_config.password.get_secret_value()
    )
    await polling_currently_playing()


if __name__ == "__main__":
    asyncio.run(main())
