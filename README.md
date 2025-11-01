# Islamic Media Recommender API

A FastAPI-based backend service that recommends movies with Islamic-lens analysis, identifying moral and ethical themes aligned with Islamic values.

## Features

- 🎬 **Movie Recommendations**: Get 3 curated movie recommendations
- 🔄 **Refresh**: Reshuffle and get new recommendations
- 🏷️ **Theme Tagging**: Automatically identify Islamic themes using sentence transformers
- 📝 **Islamic-Lens Summaries**: AI-generated summaries highlighting moral and ethical values
- 💾 **JSON Storage**: Simple file-based storage for recommendations
- 🚀 **Easy Deployment**: Ready for Vercel or Railway

## Architecture

The application consists of several modular components:

- **main.py**: FastAPI application with endpoints
- **recommendation_service.py**: Core recommendation logic
- **tmdb_client.py**: TMDb API integration for movie data
- **theme_analyzer.py**: Sentence transformers for theme identification
- **islamic_summary.py**: OpenAI integration for Islamic-perspective summaries
- **data_store.py**: JSON-based data persistence
- **config.py**: Configuration management

## API Endpoints

### `GET /`
Root endpoint with API information.

### `GET /recommend`
Get current movie recommendations (3 movies).

**Response:**
```json
{
  "recommendations": [
    {
      "id": 550,
      "title": "Fight Club",
      "overview": "A ticking-time-bomb insomniac...",
      "release_date": "1999-10-15",
      "vote_average": 8.4,
      "poster_path": "https://image.tmdb.org/t/p/w500/...",
      "backdrop_path": "https://image.tmdb.org/t/p/w500/...",
      "themes": ["struggle and perseverance", "truth and honesty"],
      "islamic_summary": "Fight Club explores themes of..."
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

## Setup

### Prerequisites

- Python 3.9+
- TMDb API key (free at https://www.themoviedb.org/settings/api)
- OpenAI API key (optional, for AI summaries)

### Installation

1. **Clone the repository:**
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
```
TMDB_API_KEY=your_tmdb_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Note: OpenAI API key is optional. If not provided, the app will use fallback summaries.

4. **Run the application:**
```bash
python main.py
```

Or using uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Deployment

### Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard:
   - `TMDB_API_KEY`
   - `OPENAI_API_KEY`

### Railway

1. Connect your GitHub repository to Railway
2. Add environment variables in Railway dashboard:
   - `TMDB_API_KEY`
   - `OPENAI_API_KEY`
3. Deploy automatically from main branch

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

## Technology Stack

- **FastAPI**: Modern Python web framework
- **TMDb API**: Movie data source
- **sentence-transformers**: Theme identification
- **OpenAI GPT-3.5**: Islamic-lens summary generation
- **JSON**: Data storage

## Project Structure

```
MTCHacks/
├── main.py                      # FastAPI application
├── config.py                    # Configuration settings
├── recommendation_service.py    # Recommendation logic
├── tmdb_client.py              # TMDb API client
├── theme_analyzer.py           # Theme analysis
├── islamic_summary.py          # Islamic summary generator
├── data_store.py               # Data persistence
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── vercel.json                # Vercel config
├── railway.json               # Railway config
└── data/                      # Data directory (auto-created)
    ├── recommendations.json   # Current recommendations
    └── movies_cache.json     # Cached movie data
```

## API Testing

You can test the API using curl:

```bash
# Get recommendations
curl http://localhost:8000/recommend

# Refresh recommendations
curl -X POST http://localhost:8000/refresh

# Health check
curl http://localhost:8000/health
```

Or visit `http://localhost:8000/docs` for interactive API documentation.

## License

MIT License
