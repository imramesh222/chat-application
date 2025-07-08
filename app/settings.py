import os
from pathlib import Path
from typing import Set
from urllib.parse import quote_plus
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self):
        # Required fields
        self.SERVICE_PORT: int = int(self._get_env("SERVICE_PORT", 8003))
        self.SECRET_KEY: str = self._get_env("SECRET_KEY", "supersecret")
        self.DATABASE_URL: str = self._get_env("DATABASE_URL")
        self.ALGORITHM: str = self._get_env("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(self._get_env("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

        # Optional fields with defaults
        self.DEBUG: bool = self._get_env("DEBUG", "True").lower() == "true"
        self.BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.TEMP_DIRECTORY: Path = Path(self._get_env("TEMP_DIRECTORY", "/tmp/"))
        self.MAX_CONTENT_LENGTH: int = int(self._get_env("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))
        self.IMAGE_ALLOWED_EXTENSIONS: Set[str] = set(
            self._get_env("IMAGE_ALLOWED_EXTENSIONS", "jpeg,pgm,webp,bmp,JPEG,JPG,jpg,png,ppm").split(","))
        self.VIDEO_ALLOWED_EXTENSIONS: Set[str] = set(
            self._get_env("VIDEO_ALLOWED_EXTENSIONS", "3gp,mp4,avi,mov,mkv,wmv,flv,webm").split(","))
        self.DOCUMENT_ALLOWED_EXTENSIONS: Set[str] = set(self._get_env("DOCUMENT_ALLOWED_EXTENSIONS", "pdf").split(","))
        self.DATABASE_HOST: str = self._get_env("DATABASE_HOST", "localhost")
        self.DATABASE_PORT: int = int(self._get_env("DATABASE_PORT", 5432))
        self.DATABASE_USER: str = self._get_env("DATABASE_USER", "postgres")
        self.DATABASE_PASSWORD: str = self._get_env("DATABASE_PASSWORD", "password")
        self.DATABASE_NAME: str = self._get_env("DATABASE_NAME", "chatapp")
        self.CHUNK_SIZE: int = int(self._get_env("CHUNK_SIZE", 512))
        self.DATABASE_PASSWORD_ENCODED: str = quote_plus(self.DATABASE_PASSWORD)
        self.ASYNC_DATABASE_URL: str = (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD_ENCODED}@"
            f"{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
        self.ALLOW_ORIGINS: Set[str] = set(self._get_env("ALLOW_ORIGINS", "*").split(","))
        self.FRONTEND_URL: str = self._get_env("FRONTEND_URL", "http://localhost:3000")

        # # Test connections
        # print(f"Service running on port: {self.SERVICE_PORT}")
        print(f"Database URL: {self.DATABASE_URL}")
        # print(f"JWT Algorithm: {self.ALGORITHM}")
        # print(f"Token Expiry (min): {self.ACCESS_TOKEN_EXPIRE_MINUTES}")
        # print(f"Service running on port: {os.getenv('SERVICE_PORT', 8003)}")

        



        


    def _get_env(self, key: str, default=None):
        value = os.getenv(key, default)
        if value is None:
            raise EnvironmentError(f"Required environment variable '{key}' is missing.")
        return value

# Instantiate the Settings class to trigger the print statements
settings = Settings()
