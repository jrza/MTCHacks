#!/usr/bin/env python3
"""
Demo script to test the Islamic Media Recommender API
This script demonstrates the functionality with mock data when API keys are not available.
"""

import json
import os
import sys

# Mock movie data for testing
MOCK_MOVIES = [
    {
        "id": 1,
        "title": "The Pursuit of Happyness",
        "overview": "A struggling salesman takes custody of his son as he's poised to begin a life-changing professional career. Based on a true story about a man's pursuit of success against all odds, showing perseverance, family bonds, and faith in difficult times.",
        "release_date": "2006-12-15",
        "vote_average": 8.0,
        "poster_path": "https://image.tmdb.org/t/p/w500/example1.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w500/backdrop1.jpg"
    },
    {
        "id": 2,
        "title": "The Blind Side",
        "overview": "The story of Michael Oher, a homeless and traumatized boy who became an All American football player with the help of a caring woman and her family. A powerful story of compassion, family, and community coming together.",
        "release_date": "2009-11-20",
        "vote_average": 7.7,
        "poster_path": "https://image.tmdb.org/t/p/w500/example2.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w500/backdrop2.jpg"
    },
    {
        "id": 3,
        "title": "12 Angry Men",
        "overview": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence. A powerful examination of justice, truth, and standing up for what is right.",
        "release_date": "1957-04-10",
        "vote_average": 8.9,
        "poster_path": "https://image.tmdb.org/t/p/w500/example3.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w500/backdrop3.jpg"
    },
    {
        "id": 4,
        "title": "Schindler's List",
        "overview": "In German-occupied Poland during World War II, Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis. A profound story of sacrifice, courage, and saving lives.",
        "release_date": "1993-12-15",
        "vote_average": 8.9,
        "poster_path": "https://image.tmdb.org/t/p/w500/example4.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w500/backdrop4.jpg"
    },
    {
        "id": 5,
        "title": "Life is Beautiful",
        "overview": "When an open-minded Jewish librarian and his son become victims of the Holocaust, he uses humor and imagination to protect his son from the horrors. A touching story of love, sacrifice, and maintaining hope in dark times.",
        "release_date": "1997-12-20",
        "vote_average": 8.6,
        "poster_path": "https://image.tmdb.org/t/p/w500/example5.jpg",
        "backdrop_path": "https://image.tmdb.org/t/p/w500/backdrop5.jpg"
    }
]

def test_theme_analyzer():
    """Test the theme analyzer"""
    print("=== Testing Theme Analyzer ===\n")
    
    from theme_analyzer import ThemeAnalyzer
    analyzer = ThemeAnalyzer()
    
    for movie in MOCK_MOVIES[:2]:
        print(f"Movie: {movie['title']}")
        themes = analyzer.get_top_themes(movie['overview'])
        print(f"Themes: {themes}\n")

def test_islamic_summary():
    """Test the Islamic summary generator"""
    print("=== Testing Islamic Summary Generator ===\n")
    
    from islamic_summary import IslamicSummaryGenerator
    generator = IslamicSummaryGenerator()
    
    movie = MOCK_MOVIES[0]
    themes = ["struggle and perseverance", "family values and relationships"]
    summary = generator.generate_summary(movie['title'], movie['overview'], themes)
    print(f"Movie: {movie['title']}")
    print(f"Themes: {themes}")
    print(f"Islamic Summary: {summary}\n")

def test_data_store():
    """Test the data store"""
    print("=== Testing Data Store ===\n")
    
    from data_store import DataStore
    store = DataStore()
    
    # Get random movies
    random_movies = store.get_random_movies(MOCK_MOVIES, 3)
    print(f"Selected {len(random_movies)} random movies:")
    for movie in random_movies:
        print(f"  - {movie['title']}")
    print()

def create_mock_cache():
    """Create mock movie cache for testing"""
    from data_store import DataStore
    store = DataStore()
    store.save_movies_cache(MOCK_MOVIES)
    print("✓ Created mock movie cache\n")

def test_full_workflow():
    """Test the full recommendation workflow"""
    print("=== Testing Full Recommendation Workflow ===\n")
    
    # Create mock cache
    create_mock_cache()
    
    # Test theme analysis
    test_theme_analyzer()
    
    # Test summary generation
    test_islamic_summary()
    
    # Test data store
    test_data_store()
    
    print("=== All Tests Passed ===")

if __name__ == "__main__":
    try:
        test_full_workflow()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
