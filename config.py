from pathlib import Path

AUTH_DIR = Path(".auth")
STORAGE_STATE = AUTH_DIR / "user.json"

BASE_URL_ENV = "BASE_URL"
TEST_USERNAME_ENV = "TEST_USER_NAME"
TEST_PASSWORD_ENV = "TEST_PASSWORD"

DEFAULT_BASE_URL = "http://frontend-ta-realworldapp.apps.os-prod.lab.proficom.de"
DEFAULT_TIMEOUT_MS = 10_000
LONG_TIMEOUT_MS = 30_000