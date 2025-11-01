"""
Theme analyzer using sentence transformers
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import config

class ThemeAnalyzer:
    """Analyzes movie themes using sentence transformers"""
    
    def __init__(self):
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.islamic_themes = config.ISLAMIC_THEMES
        # Pre-compute embeddings for Islamic themes
        self.theme_embeddings = self.model.encode(self.islamic_themes)
    
    def analyze_movie(self, movie_overview: str) -> List[Dict[str, float]]:
        """
        Analyze a movie's overview and return relevant Islamic themes
        
        Args:
            movie_overview: The movie's plot overview
            
        Returns:
            List of themes with their similarity scores
        """
        if not movie_overview:
            return []
        
        # Encode the movie overview
        overview_embedding = self.model.encode([movie_overview])[0]
        
        # Calculate cosine similarity with each theme
        similarities = []
        for i, theme in enumerate(self.islamic_themes):
            theme_embedding = self.theme_embeddings[i]
            
            # Cosine similarity
            similarity = np.dot(overview_embedding, theme_embedding) / (
                np.linalg.norm(overview_embedding) * np.linalg.norm(theme_embedding)
            )
            
            similarities.append({
                "theme": theme,
                "score": float(similarity)
            })
        
        # Sort by score and return top themes
        similarities.sort(key=lambda x: x["score"], reverse=True)
        
        # Return themes with score > 0.3 (reasonable threshold)
        return [s for s in similarities if s["score"] > 0.3][:3]
    
    def get_top_themes(self, movie_overview: str, top_n: int = 3) -> List[str]:
        """Get the top N themes for a movie"""
        themes = self.analyze_movie(movie_overview)
        return [t["theme"] for t in themes[:top_n]]
