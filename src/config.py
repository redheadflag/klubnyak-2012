from pathlib import Path

from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


PARENT_DIR = Path(__file__).parent.parent


class SpotifyConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PARENT_DIR / ".env",
        env_prefix="spotify_",
        extra="ignore"
    )

    client_id: str
    client_secret: str
    username: str
    redirect_uri: HttpUrl
    scope: str
    cache_filename: str = "spotify-token.json"
    
    refresh_time: int

    @property
    def cache_path(self) -> Path:
        return PARENT_DIR / self.cache_filename


class TelegramConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PARENT_DIR / ".env",
        env_prefix="telegram_",
        extra="ignore"
    )

    api_id: int
    api_hash: str
    phone: str
    password: SecretStr


class GeneralConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PARENT_DIR / ".env",
        extra="ignore"
    )

    output_dir: str
    remove_downloads: bool = True
    song_history_filename: str

    @property
    def output_dir_path(self) -> Path:
        return PARENT_DIR / self.output_dir
    
    @property
    def song_history_path(self) -> Path:
        return PARENT_DIR / self.song_history_filename


spotify_config = SpotifyConfig()    # type: ignore
telegram_config = TelegramConfig()  # type: ignore
general_config = GeneralConfig()    # type: ignore
