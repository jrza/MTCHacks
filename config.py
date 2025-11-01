"""
Configuration settings for the Islamic Media Recommender API
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# TMDb API Configuration
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Application Settings
DATA_FILE = "data/recommendations.json"
MOVIES_CACHE_FILE = "data/movies_cache.json"
NUM_RECOMMENDATIONS = 3

# Sentence Transformer Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

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
