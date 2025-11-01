"""
Configuration settings for the Islamic Media Recommender API
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (TMDb is now optional)
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")

# TMDb API Configuration
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Application Settings
DATA_FILE = "data/recommendations.json"
MOVIES_CACHE_FILE = "data/movies_cache.json"
NUM_RECOMMENDATIONS = 3

# Hugging Face Model Configuration
SUMMARY_MODEL = "google/flan-t5-small"  # Lightweight model for summaries
MAX_SUMMARY_LENGTH = 150
MIN_SUMMARY_LENGTH = 50

# Islamic themes to search for
ISLAMIC_THEMES = [
    "faith and spirituality",
    "family values and relationships", 
    "justice and fairness",
    "compassion and kindness",
    "struggle and perseverance",
    "truth and honesty",
    "wisdom and knowledge",
    "community and brotherhood",
    "sacrifice and selflessness",
    "redemption and forgiveness"
]
