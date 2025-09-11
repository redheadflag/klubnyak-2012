import spotipy
from spotipy.oauth2 import SpotifyOAuth

import config
from schemas import Song


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET,
    redirect_uri=config.SPOTIFY_REDIRECT_URI,
    scope=config.SPOTIFY_SCOPE
))


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
