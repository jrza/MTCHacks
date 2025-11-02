"""
Movie recommendation service - simplified
"""
from typing import List, Dict
from theme_analyzer import ThemeAnalyzer
from islamic_summary import generate_islamic_summary
from data_store import DataStore
import config
import random

class RecommendationService:
    """Service for generating and managing movie/tv recommendations"""
    
    def __init__(self):
        self.theme_analyzer = ThemeAnalyzer()
        self.data_store = DataStore()
    
    def _get_default_tv_shows(self) -> List[Dict]:
        """Return default TV shows"""
        return [
            {
                "id": 101,
                "title": "Planet Earth",
                "overview": "A groundbreaking documentary series exploring the beauty and wonder of our natural world. Showcases the majesty of creation, environmental stewardship, and the interconnectedness of all living things.",
                "release_date": "2006-03-05",
                "vote_average": 9.3,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 102,
                "title": "The Crown",
                "overview": "Chronicles the life of Queen Elizabeth II and the political and personal events that shaped her reign. Explores themes of duty, responsibility, family, and moral leadership.",
                "release_date": "2016-11-04",
                "vote_average": 8.6,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 103,
                "title": "Little House on the Prairie",
                "overview": "A family living on a farm in the 1870s faces life's challenges with faith, love, and strong family values. Shows perseverance, community support, and moral integrity in difficult times.",
                "release_date": "1974-09-11",
                "vote_average": 8.1,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 104,
                "title": "Avatar: The Last Airbender",
                "overview": "A young boy destined to bring peace to a war-torn world must master the elements and face his destiny. Explores balance, justice, wisdom, and the importance of spiritual growth.",
                "release_date": "2005-02-21",
                "vote_average": 8.9,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 105,
                "title": "Anne with an E",
                "overview": "An orphan girl with a vivid imagination finds a home and family. A touching story of kindness, acceptance, resilience, and the power of community and belonging.",
                "release_date": "2017-03-19",
                "vote_average": 8.7,
                "poster_path": None,
                "backdrop_path": None
            },
            {
                "id": 106,
                "title": "Mr. Rogers' Neighborhood",
                "overview": "Fred Rogers teaches children about kindness, empathy, and understanding through gentle lessons. Emphasizes compassion, patience, and treating others with respect and dignity.",
                "release_date": "1968-02-19",
                "vote_average": 8.5,
                "poster_path": None,
                "backdrop_path": None
            }
        ]
    
    def _get_default_movies(self) -> List[Dict]:
        """Return default movies"""
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
        """Add themes and Islamic summary to movie"""
        overview = movie.get("overview", "")
        themes = self.theme_analyzer.get_top_themes(overview)
        
        movie["themes"] = themes
        movie["islamic_summary"] = generate_islamic_summary(
            movie.get("title", ""),
            overview,
            themes
        )
        
        return movie
    
    def get_recommendations(self, content_type: str = "movie", refresh: bool = False) -> Dict:
        """Get movie or tv recommendations"""
        cache_key = f"{content_type}_recommendations"
        
        # Load cached if available and not refreshing
        if not refresh:
            saved = self.data_store.load_recommendations(cache_key)
            if saved and saved.get("recommendations"):
                return {
                    "recommendations": saved["recommendations"],
                    "count": len(saved["recommendations"])
                }
        
        # Generate new recommendations
        if content_type == "tv":
            all_content = self._get_default_tv_shows()
        else:
            all_content = self._get_default_movies()
        
        selected = random.sample(all_content, min(config.NUM_RECOMMENDATIONS, len(all_content)))
        
        recommendations = [self._enrich_movie(m.copy()) for m in selected]
        
        # Save for next time
        self.data_store.save_recommendations(recommendations, cache_key)
        
        return {
            "recommendations": recommendations,
            "count": len(recommendations)
        }
