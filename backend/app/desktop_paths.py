import os
from pathlib import Path


APP_NAME = "MyNotes AI"


def user_data_dir() -> Path:
    appdata = os.getenv("APPDATA")
    if appdata:
        return Path(appdata) / APP_NAME
    return Path.home() / ".mynotes-ai"


def resolve_database_path() -> Path:
    database_url = os.getenv("DATABASE_URL", "")
    if database_url.startswith("sqlite:///"):
        return Path(database_url.removeprefix("sqlite:///"))

    explicit_path = os.getenv("MYNOTES_DB_PATH")
    if explicit_path:
        return Path(explicit_path)

    if os.getenv("MYNOTES_ENV") == "desktop" or os.getenv("MYNOTES_USE_USER_DATA") == "1":
        return user_data_dir() / "mynotes.db"

    return Path("data/mynotes.db")
