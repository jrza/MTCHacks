"""
Simple Islamic-lens summary generator using templates
"""
from typing import List

def generate_islamic_summary(title: str, overview: str, themes: List[str]) -> str:
    """
    Generate an Islamic-lens summary for a movie using simple templates.
    
    Args:
        title: Movie title
        overview: Movie overview
        themes: List of identified Islamic themes
        
    Returns:
        Islamic-perspective summary (2-3 sentences)
    """
    if themes:
        theme_str = ", ".join(themes[:2])
        return f"{title} explores themes of {theme_str}, offering valuable insights into moral character and ethical decision-making from an Islamic perspective. The story encourages reflection on values and principles aligned with Islamic teachings."
    else:
        return f"{title} presents a story that encourages reflection on values and principles aligned with Islamic teachings. The narrative offers meaningful perspectives on character development and moral growth."
