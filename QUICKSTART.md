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

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   - Get a free TMDb API key at: https://www.themoviedb.org/settings/api
   - (Optional) Add OpenAI API key for AI-powered summaries

4. **Run the application:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

5. **View API documentation:**
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Testing Without API Keys

If you want to test the application without setting up API keys:

```bash
python demo.py
```

This will run a demonstration of the theme analyzer and summary generator with mock movie data.

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

3. **Set environment secrets:**
   ```bash
   vercel env add TMDB_API_KEY
   vercel env add OPENAI_API_KEY
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

3. **Add environment variables in Railway dashboard:**
   - `TMDB_API_KEY`
   - `OPENAI_API_KEY`

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
  "tmdb_configured": true,
  "openai_configured": true
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
┌────▼────┐   ┌──────▼─────┐  ┌────▼─────┐
│ TMDb    │   │   Theme    │  │ Islamic  │
│ Client  │   │  Analyzer  │  │ Summary  │
│         │   │            │  │ Generator│
└────┬────┘   └──────┬─────┘  └────┬─────┘
     │               │              │
     │        ┌──────▼──────────────▼─┐
     │        │    DataStore         │
     └────────►   (data_store.py)    │
              │   - JSON Storage     │
              └──────────────────────┘
```

## Key Features

1. **Modular Design**: Each component has a single responsibility
2. **Simple Storage**: JSON files for easy debugging and portability
3. **Graceful Degradation**: Works with or without OpenAI API key
4. **Theme Analysis**: Keyword-based Islamic theme identification
5. **Ready to Deploy**: Configured for Vercel and Railway

## Troubleshooting

### Port Already in Use
```bash
# Kill existing server
pkill -f "python main.py"

# Or use a different port
uvicorn main:app --port 8001
```

### API Key Issues
- Ensure `.env` file exists and contains valid keys
- Check that keys don't have extra spaces or quotes
- Verify TMDb API key at: https://www.themoviedb.org/settings/api

### Dependencies
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

## Next Steps

1. **Get API Keys**: Sign up for TMDb (required) and OpenAI (optional)
2. **Test Locally**: Run `python main.py` and visit http://localhost:8000/docs
3. **Deploy**: Choose Vercel or Railway for instant deployment
4. **Customize**: Modify Islamic themes in `config.py` to match your preferences
