"""Application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    REQUEST_TIMEOUT_SECONDS = 10
