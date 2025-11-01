# Islamic Media Recommender API

A FastAPI-based backend service that recommends movies with Islamic-lens analysis, identifying moral and ethical themes aligned with Islamic values.

## API Endpoints

### `GET /recommend`
Get current movie recommendations (3 movies).

**Response:**
```json
{
  "recommendations": [
    {
      "id": 550,
      "title": "Movie Title",
      "overview": "Movie description...",
      "release_date": "1999-10-15",
      "vote_average": 8.4,
      "poster_path": "https://image.tmdb.org/t/p/w500/...",
      "backdrop_path": "https://image.tmdb.org/t/p/w500/...",
      "themes": ["faith and spirituality", "family values"],
      "islamic_summary": "2-3 sentence Islamic-perspective summary..."
    }
  ],
  "count": 3
}
```

### `POST /refresh`
Refresh and get new random recommendations.

**Response:** Same as `/recommend`

### `GET /health`
Health check endpoint.

### `GET /`
Root endpoint with API information.

## Setup

1. Install dependencies:
```bash
py -m pip install -r requirements.txt
```

2. (Optional) Set environment variables:
```bash
TMDB_API_KEY=your_tmdb_api_key_here
ALLOWED_ORIGINS=*
```

3. Run the application:

**Windows (Git Bash/PowerShell/CMD):**
```bash
py -m uvicorn main:app --reload
```

**Or use the run script:**
```bash
# Git Bash
bash run.sh

# PowerShell/CMD
run.bat
```

The API will be available at `http://localhost:8000`

## Islamic Themes

The app identifies the following Islamic values and themes in movies:

- Faith and spirituality
- Family values and relationships
- Justice and fairness
- Compassion and kindness
- Struggle and perseverance
- Truth and honesty
- Wisdom and knowledge
- Community and brotherhood
- Sacrifice and selflessness
- Redemption and forgiveness

## Core Components

- **main.py**: FastAPI application with endpoints
- **recommendation_service.py**: Core recommendation logic
- **theme_analyzer.py**: Keyword-based theme identification
- **islamic_summary.py**: Hugging Face model for Islamic-perspective summaries
- **data_store.py**: JSON-based data persistence
- **tmdb_client.py**: Optional TMDb API integration
- **config.py**: Configuration management
