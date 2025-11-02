"""
Data storage manager for movie recommendations
"""
import json
import os
from typing import List, Dict, Optional
import random
import config

class DataStore:
    """Manages JSON-based storage for movie recommendations"""
    
    def __init__(self):
        self.data_file = config.DATA_FILE
        self.cache_file = config.MOVIES_CACHE_FILE
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
    
    def save_recommendations(self, recommendations: List[Dict], cache_key: str = "movie_recommendations"):
        """Save current recommendations to file"""
        # Load existing cache
        all_cache = {}
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    all_cache = json.load(f)
            except:
                pass
        
        # Update specific cache key
        all_cache[cache_key] = {
            "recommendations": recommendations,
            "current_index": 0
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(all_cache, f, indent=2, ensure_ascii=False)
    
    def load_recommendations(self, cache_key: str = "movie_recommendations") -> Optional[Dict]:
        """Load recommendations from file"""
        if not os.path.exists(self.data_file):
            return None
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                all_cache = json.load(f)
                return all_cache.get(cache_key)
        except Exception as e:
            print(f"Error loading recommendations: {e}")
            return None
    
    def save_movies_cache(self, movies: List[Dict]):
        """Save fetched movies to cache"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump({"movies": movies}, f, indent=2, ensure_ascii=False)
    
    def load_movies_cache(self) -> List[Dict]:
        """Load movies from cache"""
        if not os.path.exists(self.cache_file):
            return []
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("movies", [])
        except Exception as e:
            print(f"Error loading cache: {e}")
            return []
    
    def get_random_movies(self, movies: List[Dict], count: int = 3) -> List[Dict]:
        """Get random movies from a list"""
        if len(movies) <= count:
            return movies
        return random.sample(movies, count)
