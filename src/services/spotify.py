import config


import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_current_track():
    """Return (title, artist) of the currently playing track, or None if nothing is playing."""
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=config.SPOTIFY_CLIENT_ID,
        client_secret=config.SPOTIFY_CLIENT_SECRET,
        redirect_uri=config.SPOTIFY_REDIRECT_URI,
        scope=config.SPOTIFY_SCOPE
    ))

    current_track = sp.current_user_playing_track()

    if current_track and current_track['is_playing']:
        title = current_track['item']['name']
        artist = ", ".join([a['name'] for a in current_track['item']['artists']])
        return title, artist
    return None