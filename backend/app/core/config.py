"""
LIFELINE AI - Configuration Management
Environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""

    # Project Info
    PROJECT_NAME: str = "LIFELINE AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # API
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8081",
        "http://localhost:19006",
        "exp://*",
        "http://*",
        "https://*",
    ]

    # AI/LLM Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    AI_ENABLED: bool = os.getenv("AI_ENABLED", "True").lower() == "true"

    # Emergency Detection
    EMERGENCY_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("EMERGENCY_CONFIDENCE_THRESHOLD", "0.7")
    )
    CRITICAL_SEVERITY_THRESHOLD: float = float(
        os.getenv("CRITICAL_SEVERITY_THRESHOLD", "0.8")
    )

    # Hospital Search
    DEFAULT_HOSPITAL_RADIUS: float = float(os.getenv("DEFAULT_HOSPITAL_RADIUS", "10"))
    MAX_HOSPITAL_RESULTS: int = int(os.getenv("MAX_HOSPITAL_RESULTS", "10"))

    # Google Places API
    GOOGLE_PLACES_API_KEY: str = os.getenv("GOOGLE_PLACES_API_KEY", "")
    GOOGLE_PLACES_ENABLED: bool = os.getenv("GOOGLE_PLACES_ENABLED", "True").lower() == "true"

    # Voice Processing
    MAX_AUDIO_DURATION: int = int(os.getenv("MAX_AUDIO_DURATION", "60"))  # seconds
    SUPPORTED_AUDIO_FORMATS: List[str] = ["wav", "mp3", "m4a", "flac"]

    # Image Processing
    MAX_IMAGE_SIZE: int = int(os.getenv("MAX_IMAGE_SIZE", "5242880"))  # 5MB
    SUPPORTED_IMAGE_FORMATS: List[str] = ["jpg", "jpeg", "png", "webp"]

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
