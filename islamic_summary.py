"""
Hugging Face model client for generating Islamic-lens summaries
"""
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from typing import Optional
import config

class IslamicSummaryGenerator:
    """Generates Islamic-perspective summaries using Hugging Face models (fully offline)"""
    
    def __init__(self):
        """Initialize the Hugging Face model for text generation"""
        self.model_name = config.SUMMARY_MODEL
        self.tokenizer = None
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Load the Hugging Face model and tokenizer"""
        try:
            print(f"Loading model {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            
            # Set to evaluation mode for inference
            self.model.eval()
            
            # Move to GPU if available
            if torch.cuda.is_available():
                self.model = self.model.cuda()
            
            print(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Will use fallback summaries")
    
    def generate_summary(self, title: str, overview: str, themes: list) -> str:
        """
        Generate an Islamic-lens summary for a movie using Hugging Face model
        
        Args:
            title: Movie title
            overview: Movie overview
            themes: List of identified Islamic themes
            
        Returns:
            Islamic-perspective summary
        """
        # If model failed to load, use fallback
        if not self.model or not self.tokenizer:
            return self._generate_fallback_summary(title, overview, themes)
        
        try:
            theme_str = ", ".join(themes) if themes else "universal values"
            
            # Create a prompt for the model
            prompt = f"""Analyze this movie from an Islamic perspective, focusing on moral themes.

Movie: {title}
Plot: {overview}
Islamic Themes: {theme_str}

Write a 2-3 sentence summary highlighting how this movie relates to Islamic values like faith, family, justice, compassion, and moral growth. Be balanced and constructive."""

            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                max_length=512,
                truncation=True,
                return_tensors="pt"
            )
            
            # Move to GPU if available
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Generate summary
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=config.MAX_SUMMARY_LENGTH,
                    min_length=config.MIN_SUMMARY_LENGTH,
                    num_beams=4,
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    no_repeat_ngram_size=3
                )
            
            # Decode the generated summary
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up the summary
            summary = summary.strip()
            
            # If summary is too short or generic, use fallback
            if len(summary) < 20:
                return self._generate_fallback_summary(title, overview, themes)
            
            return summary
        
        except Exception as e:
            print(f"Error generating summary with model: {e}")
            return self._generate_fallback_summary(title, overview, themes)
    
    def _generate_fallback_summary(self, title: str, overview: str, themes: list) -> str:
        """Generate a simple fallback summary without AI model"""
        if themes:
            theme_str = ", ".join(themes[:2])
            return f"{title} explores themes of {theme_str}, offering valuable insights into moral character and ethical decision-making from an Islamic perspective."
        else:
            return f"{title} presents a story that encourages reflection on values and principles aligned with Islamic teachings."

