from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from config import general_config


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
    file_id: int
    access_hash: int
    file_reference: bytes = field(repr=False)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "artist": self.artist,
            "duration_sec": self.duration_sec,
            "file_id": self.file_id,
            "access_hash": self.access_hash,
            "file_reference": self.file_reference.hex(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UploadedSong":
        return cls(
            title=data["title"],
            artist=data["artist"],
            duration_sec=data["duration_sec"],
            file_id=data["file_id"],
            access_hash=data["access_hash"],
            file_reference=bytes.fromhex(data["file_reference"]),
        )


class SongHistory:
    def __init__(self, path: Path = general_config.song_history_path):
        self.path = path
        self.history: list[UploadedSong] = self.load()

    def __len__(self):
        return len(self.history)
    
    def __getitem__(self, position):
        return self.history[position]
    
    def __contains__(self, song: Song):
        return any(s.title == song.title and s.artist == song.artist for s in self.history)
    
    def add(self, song: UploadedSong) -> None:
        self.history.append(song)
        self.save()
    
    def pop(self) -> UploadedSong:
        song = self.history.pop(0)
        self.save()
        return song

    def is_same_song(self, song: Song) -> bool:
        if len(self) == 0:
            return False
        return song in self
    
    def save(self):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.history], f, indent=2)

    def load(self) -> list[UploadedSong]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [UploadedSong.from_dict(d) for d in data]
