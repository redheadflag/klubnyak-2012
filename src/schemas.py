from dataclasses import dataclass
from pathlib import Path


@dataclass
class Song:
    title: str
    artist: str
    duration_sec: int

    @property
    def as_query(self) -> str:
        return str(self)
    
    def __repr__(self) -> str:
        return f"{self.artist} — {self.title}"


@dataclass
class DownloadedSong(Song):
    path: Path



class Memory:
    def __init__(self):
        self.song: Song | None  = None
        self.file: object | None  = None

    def is_same_song(self, song) -> bool:
        return self.song is not None and str(self.song) == str(song)
