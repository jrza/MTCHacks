"""
TMDb API client for fetching movie data
"""
import requests
from typing import List, Dict, Optional
import config

class TMDbClient:
    """Client for interacting with The Movie Database API"""
    
    def __init__(self):
        self.api_key = config.TMDB_API_KEY
        self.base_url = config.TMDB_BASE_URL
        self.image_base_url = config.TMDB_IMAGE_BASE_URL
    
    def search_movies(self, query: str, page: int = 1) -> List[Dict]:
        """Search for movies by query"""
        url = f"{self.base_url}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
            "page": page,
            "language": "en-US"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            print(f"Error searching movies: {e}")
            return []
    
    def get_popular_movies(self, page: int = 1) -> List[Dict]:
        """Get popular movies"""
        url = f"{self.base_url}/movie/popular"
        params = {
            "api_key": self.api_key,
            "page": page,
            "language": "en-US"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            print(f"Error fetching popular movies: {e}")
            return []
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Get detailed information about a specific movie"""
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            "api_key": self.api_key,
            "language": "en-US"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching movie details: {e}")
            return None
    
    def get_top_rated_movies(self, page: int = 1) -> List[Dict]:
        """Get top rated movies"""
        url = f"{self.base_url}/movie/top_rated"
        params = {
            "api_key": self.api_key,
            "page": page,
            "language": "en-US"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            print(f"Error fetching top rated movies: {e}")
            return []
    
    def format_movie_data(self, movie: Dict) -> Dict:
        """Format movie data for our application"""
        return {
            "id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "vote_average": movie.get("vote_average"),
            "poster_path": f"{self.image_base_url}{movie.get('poster_path')}" if movie.get("poster_path") else None,
            "backdrop_path": f"{self.image_base_url}{movie.get('backdrop_path')}" if movie.get("backdrop_path") else None
        }
