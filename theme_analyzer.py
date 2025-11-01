"""
Theme analyzer using simple text matching
"""
from typing import List, Dict
import config
import re

class ThemeAnalyzer:
    """Analyzes movie themes using keyword matching"""
    
    def __init__(self):
        self.islamic_themes = config.ISLAMIC_THEMES
        # Keywords associated with each theme
        self.theme_keywords = {
            "faith and spirituality": ["faith", "belief", "god", "religion", "spiritual", "prayer", "divine", "soul"],
            "family values and relationships": ["family", "father", "mother", "son", "daughter", "parent", "sibling", "brother", "sister", "marriage", "home"],
            "justice and fairness": ["justice", "fair", "right", "wrong", "law", "truth", "equality", "court", "judge"],
            "compassion and kindness": ["compassion", "kind", "mercy", "caring", "help", "gentle", "empathy", "love", "generous"],
            "struggle and perseverance": ["struggle", "fight", "battle", "overcome", "persevere", "endure", "challenge", "survive", "courage"],
            "truth and honesty": ["truth", "honest", "lie", "deception", "integrity", "authentic", "genuine", "trust"],
            "wisdom and knowledge": ["wisdom", "knowledge", "learn", "teach", "understand", "education", "enlighten", "sage"],
            "community and brotherhood": ["community", "together", "unity", "brotherhood", "solidarity", "team", "group", "society"],
            "sacrifice and selflessness": ["sacrifice", "selfless", "give", "hero", "martyr", "devotion", "dedication", "duty"],
            "redemption and forgiveness": ["redemption", "forgive", "mercy", "repent", "change", "transform", "salvation", "regret"]
        }
    
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
        
        overview_lower = movie_overview.lower()
        word_tokens = set(re.findall(r'\b\w+\b', overview_lower))
        
        # Calculate scores based on keyword matches
        theme_scores = []
        for theme in self.islamic_themes:
            keywords = self.theme_keywords.get(theme, [])
            matches = sum(1 for keyword in keywords if keyword in overview_lower)
            
            # Normalize score (0-1 range)
            score = min(matches / 3.0, 1.0) if keywords else 0.0
            
            if score > 0:
                theme_scores.append({
                    "theme": theme,
                    "score": float(score)
                })
        
        # Sort by score and return top themes
        theme_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Return themes with score > 0.15 (reasonable threshold)
        return [s for s in theme_scores if s["score"] > 0.15][:3]
    
    def get_top_themes(self, movie_overview: str, top_n: int = 3) -> List[str]:
        """Get the top N themes for a movie"""
        themes = self.analyze_movie(movie_overview)
        return [t["theme"] for t in themes[:top_n]]

