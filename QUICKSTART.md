# Quick Start Guide

## For Developers

### Local Development Setup

1. **Clone and navigate to the repository:**
   ```bash
   git clone https://github.com/jrza/MTCHacks.git
   cd MTCHacks
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Note: First run will download Hugging Face model (~250MB). Subsequent runs are fully offline.

3. **Set up environment variables (optional):**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` to add TMDb API key (optional):
   - Get a free TMDb API key at: https://www.themoviedb.org/settings/api
   - Without API key, app uses cached/default movie data

4. **Run the application:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

5. **View API documentation:**
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Running Fully Offline

The application runs completely offline with no API keys required:

```bash
python demo.py
```

This will run a demonstration using:
- Open-source Hugging Face models (Flan-T5) for summaries
- Default movie dataset (no API needed)
- Keyword-based theme analysis

## For Deployment

### Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **(Optional) Set environment secrets:**
   ```bash
   vercel env add TMDB_API_KEY
   vercel env add ALLOWED_ORIGINS
   ```

### Railway

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login and init:**
   ```bash
   railway login
   railway init
   ```

3. **(Optional) Add environment variables in Railway dashboard:**
   - `TMDB_API_KEY` - for fresh movie data
   - `ALLOWED_ORIGINS` - for CORS security

4. **Deploy:**
   ```bash
   railway up
   ```

## API Usage Examples

### Get Recommendations

```bash
curl http://localhost:8000/recommend
```

**Response:**
```json
{
  "recommendations": [
    {
      "id": 550,
      "title": "Example Movie",
      "overview": "Movie description...",
      "release_date": "2020-01-01",
      "vote_average": 8.5,
      "poster_path": "https://...",
      "backdrop_path": "https://...",
      "themes": ["faith and spirituality", "family values"],
      "islamic_summary": "This movie explores..."
    }
  ],
  "count": 3
}
```

### Refresh Recommendations

```bash
curl -X POST http://localhost:8000/refresh
```

Returns 3 new random movie recommendations.

### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "tmdb_configured": false,
  "model_info": {
    "summary_model": "google/flan-t5-small",
    "runs_offline": true
  }
}
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                        (main.py)                        │
└────────────────────┬────────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
┌─────────▼─────────┐  ┌────────▼────────┐
│  /recommend       │  │   /refresh      │
│  GET endpoint     │  │   POST endpoint │
└─────────┬─────────┘  └────────┬────────┘
          │                     │
          └──────────┬──────────┘
                     │
          ┌──────────▼───────────┐
          │ RecommendationService│
          │ (recommendation_     │
          │  service.py)         │
          └──────────┬───────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
┌────▼────┐   ┌──────▼─────┐  ┌────▼─────────┐
│ TMDb    │   │   Theme    │  │ Hugging Face │
│ Client  │   │  Analyzer  │  │  Summary     │
│(Optional│   │            │  │ (Flan-T5)    │
└────┬────┘   └──────┬─────┘  └────┬─────────┘
     │               │              │
     │        ┌──────▼──────────────▼─┐
     │        │    DataStore         │
     └────────►   (data_store.py)    │
              │   - JSON Storage     │
              │   - Offline Fallback │
              └──────────────────────┘
```

## Key Features

1. **Modular Design**: Each component has a single responsibility
2. **Simple Storage**: JSON files for easy debugging and portability
3. **Fully Offline**: Runs completely offline using Hugging Face models
4. **Theme Analysis**: Keyword-based Islamic theme identification
5. **Ready to Deploy**: Configured for Vercel and Railway
6. **No API Keys Required**: Works out-of-the-box with default data

## Troubleshooting

### Port Already in Use
```bash
# Kill existing server
pkill -f "python main.py"

# Or use a different port
uvicorn main:app --port 8001
```

### Model Download Issues
- First run downloads ~250MB Flan-T5 model from Hugging Face
- Ensure stable internet connection for initial download
- Model is cached locally for offline use afterward

### TMDb API (Optional)
- App works without TMDb API key (uses cached/default data)
- To use fresh movie data, get free key at: https://www.themoviedb.org/settings/api

### Dependencies
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. **Install Dependencies**: Run `pip install -r requirements.txt` (includes Hugging Face models)
2. **Test Locally**: Run `python main.py` and visit http://localhost:8000/docs
3. **(Optional) Get TMDb Key**: For fresh movie data, sign up at https://www.themoviedb.org
4. **Deploy**: Choose Vercel or Railway for instant deployment
4. **Customize**: Modify Islamic themes in `config.py` to match your preferences
