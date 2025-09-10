import config

import os
import subprocess


def create_silent_audio(filename, title, artist):
    """Create a 1-second silent MP3 with given title and artist metadata."""
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(config.OUTPUT_DIR, filename)

    command = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo",
        "-t", "1",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-y",
        filepath
    ]
    subprocess.run(command, check=True)
    return filepath