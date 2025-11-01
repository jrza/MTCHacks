"""
Hugging Face model client for generating Islamic-lens summaries
"""
from transformers import pipeline
import config

class IslamicSummaryGenerator:
    """Generates Islamic-perspective summaries using Hugging Face models (fully offline)"""
    
    def __init__(self):
        """Initialize the Hugging Face summarization pipeline"""
        self.model_name = "sshleifer/distilbart-cnn-12-6"
        self.summarizer = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Load the Hugging Face summarization pipeline"""
        try:
            print(f"Loading summarization model {self.model_name}...")
            self.summarizer = pipeline("summarization", model=self.model_name)
            print(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Will use fallback summaries")
            self.summarizer = None
    
    def generate_summary(self, title: str, overview: str, themes: list) -> str:
        """
        Generate an Islamic-lens summary for a movie using Hugging Face summarization model
        
        Args:
            title: Movie title
            overview: Movie overview
            themes: List of identified Islamic themes
            
        Returns:
            Islamic-perspective summary (2-3 sentences)
        """
        # If model failed to load, use fallback
        if not self.summarizer:
            return self._generate_fallback_summary(title, overview, themes)
        
        try:
            theme_str = ", ".join(themes) if themes else "universal values"
            
            # Create input text for summarization
            # Focus on Islamic moral themes and values
            input_text = f"""Movie: {title}. {overview}. This film highlights Islamic themes including {theme_str}. From an Islamic perspective, the story demonstrates values such as faith, family, justice, compassion, and moral growth."""
            
            # Generate 2-3 sentence summary
            result = self.summarizer(
                input_text,
                max_length=100,  # Target length for 2-3 sentences
                min_length=30,   # Minimum length
                do_sample=False  # Deterministic summary
            )
            
            summary = result[0]['summary_text'].strip()
            
            # Add Islamic context to the summary
            if themes:
                theme_context = f" The film particularly resonates with themes of {', '.join(themes[:2])}."
                summary = summary + theme_context
            
            # Ensure summary is reasonable length
            if len(summary) < 20:
                return self._generate_fallback_summary(title, overview, themes)
            
            return summary
        
        except Exception as e:
            print(f"Error generating summary with model: {e}")
            return self._generate_fallback_summary(title, overview, themes)
    
    def _generate_fallback_summary(self, title: str, overview: str, themes: list) -> str:
        """Generate a simple fallback summary template if model fails"""
        if themes:
            theme_str = ", ".join(themes[:2])
            return f"{title} explores themes of {theme_str}, offering valuable insights into moral character and ethical decision-making from an Islamic perspective. The story encourages reflection on values and principles aligned with Islamic teachings."
        else:
            return f"{title} presents a story that encourages reflection on values and principles aligned with Islamic teachings. The narrative offers meaningful perspectives on character development and moral growth."


# Singleton instance for the generator
_generator_instance = None

def generate_islamic_summary(title: str, overview: str, themes: list) -> str:
    """
    Generate an Islamic-lens summary for a movie.
    
    Args:
        title: Movie title
        overview: Movie overview
        themes: List of identified Islamic themes
        
    Returns:
        Islamic-perspective summary (2-3 sentences)
    """
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = IslamicSummaryGenerator()
    return _generator_instance.generate_summary(title, overview, themes)

