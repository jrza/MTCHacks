"""
Movie recommendation service
"""
from typing import List, Dict
from tmdb_client import TMDbClient
from theme_analyzer import ThemeAnalyzer
from islamic_summary import IslamicSummaryGenerator
from data_store import DataStore
import config

class RecommendationService:
    """Service for generating and managing movie recommendations"""
    
    def __init__(self):
        self.tmdb = TMDbClient()
        self.theme_analyzer = ThemeAnalyzer()
        self.summary_generator = IslamicSummaryGenerator()
        self.data_store = DataStore()
        self._movie_pool = []
    
    def _fetch_movies(self) -> List[Dict]:
        """Fetch movies from TMDb API"""
        # Try to load from cache first
        cached_movies = self.data_store.load_movies_cache()
        if cached_movies and len(cached_movies) >= 10:
            return cached_movies
        
        # Fetch fresh movies
        movies = []
        
        # Get top rated movies (tend to have better themes)
        top_rated = self.tmdb.get_top_rated_movies(page=1)
        movies.extend(top_rated[:10])
        
        # Get popular movies
        popular = self.tmdb.get_popular_movies(page=1)
        movies.extend(popular[:10])
        
        # Format and deduplicate
        formatted_movies = []
        seen_ids = set()
        
        for movie in movies:
            if movie.get("id") not in seen_ids and movie.get("overview"):
                formatted_movies.append(self.tmdb.format_movie_data(movie))
                seen_ids.add(movie.get("id"))
        
        # Cache the movies
        if formatted_movies:
            self.data_store.save_movies_cache(formatted_movies)
        
        return formatted_movies
    
    def _enrich_movie(self, movie: Dict) -> Dict:
        """Enrich movie data with themes and Islamic summary"""
        overview = movie.get("overview", "")
        
        # Analyze themes
        themes = self.theme_analyzer.get_top_themes(overview)
        
        # Generate Islamic summary
        islamic_summary = self.summary_generator.generate_summary(
            movie.get("title", ""),
            overview,
            themes
        )
        
        # Add enriched data
        movie["themes"] = themes
        movie["islamic_summary"] = islamic_summary
        
        return movie
    
    def get_recommendations(self, refresh: bool = False) -> List[Dict]:
        """
        Get movie recommendations
        
        Args:
            refresh: If True, fetch new recommendations
            
        Returns:
            List of recommended movies
        """
        # If refresh or no saved recommendations, generate new ones
        if refresh:
            return self._generate_new_recommendations()
        
        # Try to load existing recommendations
        saved_data = self.data_store.load_recommendations()
        if saved_data and saved_data.get("recommendations"):
            return saved_data["recommendations"]
        
        # Generate new if none exist
        return self._generate_new_recommendations()
    
    def _generate_new_recommendations(self) -> List[Dict]:
        """Generate new movie recommendations"""
        # Fetch movie pool
        self._movie_pool = self._fetch_movies()
        
        if not self._movie_pool:
            return []
        
        # Select random movies
        selected_movies = self.data_store.get_random_movies(
            self._movie_pool,
            config.NUM_RECOMMENDATIONS
        )
        
        # Enrich with themes and summaries
        recommendations = [self._enrich_movie(movie.copy()) for movie in selected_movies]
        
        # Save recommendations
        self.data_store.save_recommendations(recommendations)
        
        return recommendations
