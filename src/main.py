import asyncio

from config import (
    spotify_config,
    general_config,
    telegram_config
)
from schemas import SongHistory
from services import (
    spotify,
    telegram,
    youtube
)


song_history = SongHistory()


async def polling_currently_playing() -> None:
    try:
        while True:
            song = spotify.get_current_track()    
            if not song:
                print("No song is playing now")
                await asyncio.sleep(spotify_config.refresh_time)
                continue
            if song_history.is_same_song(song):
                print(f"The same song is playing. Sleep for {spotify_config.refresh_time}s")
                await asyncio.sleep(spotify_config.refresh_time)
                continue
            try:
                downloaded_song = youtube.search_and_download(song=song)
            except ValueError:
                print(f"Song not found. Sleep for {song.duration_sec}s")
                await asyncio.sleep(song.duration_sec)
                continue
            
            uploaded_song = await telegram.send_to_favorites(downloaded_song=downloaded_song)
            
            await telegram.add_to_profile(uploaded_song)
            
            if len(song_history) >= 5:
                await asyncio.sleep(0.5)
                await telegram.remove_from_profile(song_history.pop())

            if general_config.remove_downloads:
                downloaded_song.path.unlink(missing_ok=True)

            song_history.add(uploaded_song)

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
