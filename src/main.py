import asyncio
from services.ffmpeg import create_silent_audio
from services.spotify import get_current_track
from services.telegram import send_to_favorites
from services.telegram import add_to_profile


async def main():
    track_info = get_current_track()
    if track_info:
        title, artist = track_info
        safe_filename = f"{title} - {artist}.mp3".replace("/", "-")
        print(f"Creating silent audio for: {title} — {artist}")
        filepath = create_silent_audio(safe_filename, title, artist)

        file = await send_to_favorites(filepath, caption=f"{title} — {artist}")
        await add_to_profile(file.document.id, file.document.access_hash, file.document.file_reference)
    else:
        print("No track is currently playing.")


if __name__ == "__main__":
    asyncio.run(main())
