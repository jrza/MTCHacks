# Offline Architecture - Islamic Media Recommender

## Overview

The Islamic Media Recommender has been redesigned to run **fully offline** using open-source Hugging Face models instead of proprietary APIs.

## Key Changes

### 1. OpenAI Replacement

**Before:**
- Used OpenAI GPT-3.5 API for Islamic-lens summaries
- Required `OPENAI_API_KEY` environment variable
- Online dependency for every summary generation

**After:**
- Uses Hugging Face `google/flan-t5-small` model
- No API key required
- Runs completely offline after initial model download
- Model cached locally (~250MB)

### 2. TMDb API - Now Optional

**Before:**
- TMDb API key was required
- Application failed without API access

**After:**
- TMDb API is completely optional
- Three-tier fallback system:
  1. **TMDb API** (if `TMDB_API_KEY` provided)
  2. **Cached Data** (from previous API calls)
  3. **Default Dataset** (6 curated movies built-in)

### 3. Dependencies Updated

**Removed:**
```
openai==1.3.0
```

**Added:**
```
transformers==4.35.0
torch==2.1.0
sentencepiece==0.1.99
```

## Architecture Flow

```
User Request
     ↓
FastAPI Endpoint
     ↓
RecommendationService
     ↓
┌────────────────┬────────────────┬──────────────────┐
│                │                │                  │
TMDb Client      Theme Analyzer   HuggingFace Model
(Optional)       (Keyword-based)  (Flan-T5)
│                │                │
└────────────────┴────────────────┴──────────────────┘
                     ↓
              JSON Data Store
        (Cache + Default Movies)
```

## Offline Operation

### First Run
1. Downloads Flan-T5 model from Hugging Face (~250MB)
2. Model cached in `~/.cache/huggingface/`
3. Uses default movie dataset if no TMDb key

### Subsequent Runs
1. Loads cached model (fully offline)
2. Uses cached/default movie data
3. No internet required

## Default Movie Dataset

Built-in movies for offline operation:
1. The Pursuit of Happyness
2. The Blind Side
3. 12 Angry Men
4. Schindler's List
5. Life is Beautiful
6. To Kill a Mockingbird

## Summary Generation

### Prompt Engineering
The Flan-T5 model receives a structured prompt:

```
Analyze this movie from an Islamic perspective, focusing on moral themes.

Movie: [Title]
Plot: [Overview]
Islamic Themes: [Detected Themes]

Write a 2-3 sentence summary highlighting how this movie relates to 
Islamic values like faith, family, justice, compassion, and moral growth.
Be balanced and constructive.
```

### Generation Parameters
- `max_length`: 150 tokens
- `min_length`: 50 tokens
- `num_beams`: 4 (beam search)
- `temperature`: 0.7
- `top_p`: 0.9
- `no_repeat_ngram_size`: 3

### Fallback
If model generation fails or produces low-quality output:
```python
f"{title} explores themes of {themes}, offering valuable insights into 
moral character and ethical decision-making from an Islamic perspective."
```

## Environment Variables

### Required
None! The app runs with zero configuration.

### Optional
- `TMDB_API_KEY`: For fresh movie data from TMDb
- `ALLOWED_ORIGINS`: For CORS security in production

## Benefits

1. **No API Costs**: Zero ongoing costs (no OpenAI subscription)
2. **Privacy**: All processing happens locally
3. **Reliability**: No dependency on external API uptime
4. **Speed**: No network latency after initial setup
5. **Portability**: Runs anywhere Python + dependencies work

## Limitations

1. **Model Size**: ~250MB initial download
2. **Quality**: Flan-T5-small less sophisticated than GPT-3.5
3. **First Run**: Requires internet for model download
4. **Compute**: Requires CPU/GPU for inference (fast on modern hardware)

## Deployment Considerations

### Vercel
- Model will be downloaded on first cold start
- Subsequent requests use cached model
- Consider serverless function timeout limits

### Railway
- Persistent storage helps with model caching
- Better suited for ML workloads
- Recommended for production

### Docker
- Include model in Docker image to avoid download on each deploy
- Pre-download model in Dockerfile for faster startup

## Performance

### Summary Generation
- First summary: 2-5 seconds (model loading)
- Subsequent: 0.5-2 seconds (inference only)
- GPU: <0.5 seconds per summary
- CPU: 1-2 seconds per summary

### Memory Usage
- Model: ~250MB in memory
- Total app: ~400-500MB typical

## Testing Offline

```bash
# Ensure no environment variables set
unset TMDB_API_KEY

# Run the app
python main.py

# Test endpoint
curl http://localhost:8000/recommend

# Should return recommendations using default movies
```

## Future Enhancements

1. **Larger Model**: Upgrade to Flan-T5-base for better quality
2. **Quantization**: Use 8-bit quantization to reduce memory
3. **Model Choice**: Allow configuration of different HF models
4. **Pre-generation**: Generate summaries in advance for common movies
5. **Caching**: Cache generated summaries to avoid re-computation

## Conclusion

The offline architecture maintains all functionality while eliminating API dependencies, costs, and privacy concerns. The app truly runs "anywhere" with just Python and the initial model download.
