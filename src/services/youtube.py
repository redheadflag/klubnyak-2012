from pathlib import Path
import yt_dlp

import config
from schemas import DownloadedSong, Song


def modify_metadata(info):
    """Return a metadata dictionary with updated title."""
    metadata = {}

    # Keep original title if exists, else fallback
    original_title = info.get("title", "Unknown Title")
    metadata["title"] = f"[Now playing] {original_title}"

    # Keep other fields if present
    if "artist" in info:
        metadata["artist"] = info["artist"]
    if "album" in info:
        metadata["album"] = info["album"]

    return metadata


def search_and_download(song: Song, tolerance: int = 5, max_results: int = 5) -> DownloadedSong:
    # ytsearch will return metadata about videos
    ydl_opts = {
        "quiet": True,
        "skip_download": True,  # first only get metadata
        "extract_flat": True,
        "noplaylist": True,
    }

    search_query = f"ytsearch{max_results}:{song.as_query}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(search_query, download=False)
    
    if not search_results:
        raise ValueError("No videos found")
    if not (results := search_results.get("entries", None)):
        raise ValueError("No videos found")
    
    filtered_videos = []
    for entry in results:
        duration = entry.get("duration")
        if duration is None:
            continue
        if song.duration_sec - tolerance <= duration <= song.duration_sec + tolerance:
            filtered_videos.append(entry)

    if not filtered_videos:
        raise ValueError("No videos found within the length constraints.") 

    # Download first match
    first_video = filtered_videos[0]
    ydl_opts_download = {
        "format": "bestaudio/best",
        "outtmpl": str(config.OUTPUT_DIR / f"{str(song)}.%(ext)s"),
        "noplaylist": True,
        "postprocessors": [
            {  # Extract audio using ffmpeg and convert to mp3
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",  # kbps
            },
        ],
        'postprocessor_args': [
            '-metadata', f'title={song.title}',  # TODO: add prefix (from config)
            '-metadata', f'artist={song.artist}',
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
        info = ydl.extract_info(first_video["url"], download=True)
        song_path = Path(info["requested_downloads"][0]["filepath"])
        return DownloadedSong(
            title=song.title,
            artist=song.artist,
            duration_sec=song.duration_sec,
            path=song_path
        )
