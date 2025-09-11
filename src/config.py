from pathlib import Path

# =====================
# Spotify API
# =====================
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
SPOTIFY_SCOPE = "user-read-currently-playing"

SPOTIFY_REFRESH_TIME = 10

# =====================
# Telegram API
# =====================
TELEGRAM_API_ID =               # from https://my.telegram.org
TELEGRAM_API_HASH = ""

TELEGRAM_PHONE = "+"
TELEGRAM_PASSWORD = ""

# =====================
# General
# =====================
PARENT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = PARENT_DIR / "output"                   # folder to store generated files
REMOVE_DOWNLOADS = True