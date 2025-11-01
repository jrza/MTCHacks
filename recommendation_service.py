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
        """Fetch movies from TMDb API or use cached data as fallback"""
        # Try to load from cache first
        cached_movies = self.data_store.load_movies_cache()
        
        # If TMDb API is available, try to fetch fresh movies
        if self.tmdb.api_available:
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
            
            # Cache the movies if we got any
            if formatted_movies:
                self.data_store.save_movies_cache(formatted_movies)
                return formatted_movies
            
            # If API call failed but we have cache, use it
            if cached_movies:
                print("TMDb API call failed, using cached data")
                return cached_movies
        else:
            # TMDb API not available, use cached data
            if cached_movies:
                print("Using cached movie data (TMDb API not configured)")
                return cached_movies
            else:
                # No cache and no API - use default movies
                print("No cache available and TMDb API not configured - using default movies")
                return self._get_default_movies()
        
        return []
    
    def _get_default_movies(self) -> List[Dict]:
        """Return a set of default movies when no API or cache is available"""
        return [
            {
                "id": 1,
                "title": "The Pursuit of Happyness",
                "overview": "A struggling salesman takes custody of his son as he's poised to begin a life-changing professional career. Based on a true story about a man's pursuit of success against all odds, showing perseverance, family bonds, and faith in difficult times.",
                "release_date": "2006-12-15",
                "vote_average": 8.0,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 2,
                "title": "The Blind Side",
                "overview": "The story of Michael Oher, a homeless and traumatized boy who became an All American football player with the help of a caring woman and her family. A powerful story of compassion, family, and community coming together.",
                "release_date": "2009-11-20",
                "vote_average": 7.7,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 3,
                "title": "12 Angry Men",
                "overview": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence. A powerful examination of justice, truth, and standing up for what is right.",
                "release_date": "1957-04-10",
                "vote_average": 8.9,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 4,
                "title": "Schindler's List",
                "overview": "In German-occupied Poland during World War II, Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis. A profound story of sacrifice, courage, and saving lives.",
                "release_date": "1993-12-15",
                "vote_average": 8.9,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 5,
                "title": "Life is Beautiful",
                "overview": "When an open-minded Jewish librarian and his son become victims of the Holocaust, he uses humor and imagination to protect his son from the horrors. A touching story of love, sacrifice, and maintaining hope in dark times.",
                "release_date": "1997-12-20",
                "vote_average": 8.6,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 6,
                "title": "To Kill a Mockingbird",
                "overview": "A lawyer in Depression-era Alabama defends a black man against an undeserved rape charge. A story of justice, integrity, and standing up for what is right despite social pressure.",
                "release_date": "1962-12-25",
                "vote_average": 8.4,
                "poster_path": None,
                "backdrop_path": None
            }
        ]
    
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
