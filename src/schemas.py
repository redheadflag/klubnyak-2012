from dataclasses import dataclass
from pathlib import Path

from telethon.types import Document


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


@dataclass
class UploadedSong(Song):
    document: Document


class SongHistory:
    def __init__(self):
        self.history: list[UploadedSong] = []

    def __len__(self):
        return len(self.history)
    
    def __getitem__(self, position):
        return self.history[position]
    
    def __contains__(self, song: Song):
        return any(s.title == song.title and s.artist == song.artist for s in self.history)
    
    def add(self, song: UploadedSong) -> None:
        self.history.append(song)
    
    def pop(self) -> UploadedSong:
        return self.history.pop(0)

    def is_same_song(self, song: Song) -> bool:
        if len(self) == 0:
            return False
        return song in self
