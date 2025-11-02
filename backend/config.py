"""
Configuration settings for the Islamic Media Recommender API
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Application Settings
DATA_FILE = "data/recommendations.json"
MOVIES_CACHE_FILE = "data/movies_cache.json"
NUM_RECOMMENDATIONS = 3

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
