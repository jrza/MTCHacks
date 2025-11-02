"""
FastAPI application for CineDeen - Islamic Media Recommender
Run with: python main.py
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from recommendation_service import RecommendationService

app = FastAPI(
    title="CineDeen API",
    description="Islamic Media Recommender API",
    version="1.0.0"
)

# CORS - allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
recommendation_service = RecommendationService()

class MovieRecommendation(BaseModel):
    id: int
    title: str
    overview: str
    release_date: str
    vote_average: float
    poster_path: Optional[str]
    backdrop_path: Optional[str]
    themes: List[str]
    islamic_summary: str

class RecommendationsResponse(BaseModel):
    recommendations: List[MovieRecommendation]
    count: int

@app.get("/")
async def root():
    return {"message": "CineDeen API", "version": "1.0.0"}

@app.get("/recommend", response_model=RecommendationsResponse)
async def get_recommendations(type: str = "movie"):
    """Get current recommendations (movie or tv)"""
    return recommendation_service.get_recommendations(content_type=type, refresh=False)

@app.post("/refresh", response_model=RecommendationsResponse)
async def refresh_recommendations(type: str = "movie"):
    """Refresh recommendations with new random content"""
    return recommendation_service.get_recommendations(content_type=type, refresh=True)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("Starting CineDeen API server on http://127.0.0.1:8000")
    print("Press CTRL+C to stop")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
