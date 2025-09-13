import spotipy
from spotipy.cache_handler import CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth

from config import spotify_config, PARENT_DIR
from schemas import Song


cache_handler = CacheFileHandler(
    cache_path=spotify_config.cache_path,
    username=spotify_config.username
)


auth_manager = SpotifyOAuth(
    client_id=spotify_config.client_id,
    client_secret=spotify_config.client_secret,
    redirect_uri=str(spotify_config.redirect_uri),
    scope=spotify_config.scope,
    cache_handler=cache_handler
)


sp = spotipy.Spotify(auth_manager=auth_manager)


def get_current_track() -> Song | None:
    """Return Song instance of the currently playing track, or None if nothing is playing."""

    current_track = sp.current_user_playing_track()

    if current_track and current_track['is_playing']:
        item = current_track.get("item", None)
        if not item:
            return None
        title = item.get("name", None)
        if not title:
            return None
        artist = ", ".join([a['name'] for a in current_track['item']['artists']])
        duration = current_track['item']['duration_ms'] // 1000
        return Song(title, artist, duration)
    return None
