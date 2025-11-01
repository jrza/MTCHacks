"""
OpenAI client for generating Islamic-lens summaries
"""
from openai import OpenAI
from typing import Optional
import config

class IslamicSummaryGenerator:
    """Generates Islamic-perspective summaries using OpenAI"""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY) if config.OPENAI_API_KEY else None
    
    def generate_summary(self, title: str, overview: str, themes: list) -> str:
        """
        Generate an Islamic-lens summary for a movie
        
        Args:
            title: Movie title
            overview: Movie overview
            themes: List of identified Islamic themes
            
        Returns:
            Islamic-perspective summary
        """
        if not self.client:
            # Fallback if no API key
            return self._generate_fallback_summary(title, overview, themes)
        
        try:
            theme_str = ", ".join(themes) if themes else "universal values"
            
            prompt = f"""You are an Islamic media analyst. Analyze this movie from an Islamic perspective, focusing on moral and ethical themes.

Movie: {title}
Overview: {overview}
Identified Themes: {theme_str}

Provide a 2-3 sentence summary highlighting how this movie's themes relate to Islamic values such as faith, family, justice, compassion, and moral growth. Be balanced and constructive."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a thoughtful Islamic media analyst who identifies positive moral themes in films."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating OpenAI summary: {e}")
            return self._generate_fallback_summary(title, overview, themes)
    
    def _generate_fallback_summary(self, title: str, overview: str, themes: list) -> str:
        """Generate a simple fallback summary without OpenAI"""
        if themes:
            theme_str = ", ".join(themes[:2])
            return f"{title} explores themes of {theme_str}, offering valuable insights into moral character and ethical decision-making."
        else:
            return f"{title} presents a story that encourages reflection on values and principles."
