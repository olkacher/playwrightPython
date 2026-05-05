import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env once
load_dotenv()


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"{name} is not set")
    return value


def _get_int(name: str, default: int) -> int:
    return int(os.getenv(name, default))


# Paths
AUTH_DIR = Path(".auth")
STORAGE_STATE = AUTH_DIR / "user.json"

# Config values
BASE_URL = _get_env("BASE_URL", "http://frontend-ta-realworldapp.apps.os-prod.lab.proficom.de")

TEST_USERNAME = _get_env("TEST_USER_NAME")
TEST_PASSWORD = _get_env("TEST_PASSWORD")

DEFAULT_TIMEOUT_MS = _get_int("DEFAULT_TIMEOUT_MS", 10_000)
LONG_TIMEOUT_MS = _get_int("LONG_TIMEOUT_MS", 30_000)