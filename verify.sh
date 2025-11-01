#!/bin/bash
# Verification script for Islamic Media Recommender API

echo "=== Islamic Media Recommender API - Verification ==="
echo ""

# Check Python version
echo "1. Checking Python version..."
python3 --version || { echo "❌ Python 3 not found"; exit 1; }
echo "✓ Python found"
echo ""

# Check if all required files exist
echo "2. Checking required files..."
files=("main.py" "config.py" "tmdb_client.py" "theme_analyzer.py" "islamic_summary.py" "data_store.py" "recommendation_service.py" "requirements.txt" ".env.example" "README.md" "vercel.json" "railway.json")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ❌ $file missing"
        exit 1
    fi
done
echo ""

# Check syntax of Python files
echo "3. Checking Python syntax..."
for pyfile in *.py; do
    python3 -m py_compile "$pyfile" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  ✓ $pyfile"
    else
        echo "  ❌ $pyfile has syntax errors"
        exit 1
    fi
done
echo ""

# Check if .env exists or can be created
echo "4. Checking environment configuration..."
if [ -f ".env" ]; then
    echo "  ✓ .env file exists"
else
    echo "  ⚠ .env file not found (copy from .env.example)"
fi
echo ""

# Summary
echo "=== Verification Complete ==="
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and add your API keys"
echo "  2. Install dependencies: pip install -r requirements.txt"
echo "  3. Run the server: python main.py"
echo "  4. Visit http://localhost:8000/docs for API documentation"
echo ""
