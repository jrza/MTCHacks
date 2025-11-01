"""
FastAPI application for Islamic Media Recommender
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from recommendation_service import RecommendationService
import config
import os

app = FastAPI(
    title="Islamic Media Recommender API",
    description="API for recommending movies with Islamic-lens analysis",
    version="1.0.0"
)

# CORS middleware for frontend integration
# For production, set ALLOWED_ORIGINS environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommendation service
recommendation_service = RecommendationService()

class MovieRecommendation(BaseModel):
    """Movie recommendation model"""
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
    """Response model for recommendations"""
    recommendations: List[MovieRecommendation]
    count: int

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Islamic Media Recommender API",
        "version": "1.0.0",
        "endpoints": {
            "/recommend": "GET - Get current movie recommendations",
            "/refresh": "POST - Refresh and get new recommendations"
        }
    }

@app.get("/recommend", response_model=RecommendationsResponse)
async def get_recommendations():
    """
    Get current movie recommendations
    
    Returns 3 movies with Islamic-lens analysis
    """
    try:
        recommendations = recommendation_service.get_recommendations(refresh=False)
        
        if not recommendations:
            raise HTTPException(
                status_code=500,
                detail="Unable to fetch recommendations. Please check API configuration."
            )
        
        return {
            "recommendations": recommendations,
            "count": len(recommendations)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching recommendations: {str(e)}"
        )

@app.post("/refresh", response_model=RecommendationsResponse)
async def refresh_recommendations():
    """
    Refresh recommendations with new random movies
    
    Returns 3 new movies with Islamic-lens analysis
    """
    try:
        recommendations = recommendation_service.get_recommendations(refresh=True)
        
        if not recommendations:
            raise HTTPException(
                status_code=500,
                detail="Unable to fetch recommendations. Please check API configuration."
            )
        
        return {
            "recommendations": recommendations,
            "count": len(recommendations)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error refreshing recommendations: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "tmdb_configured": bool(config.TMDB_API_KEY),
        "openai_configured": bool(config.OPENAI_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
