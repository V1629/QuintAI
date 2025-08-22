#!/bin/bash

echo "🚀 Starting QuintAI Production Server..."

# Check if we're in production environment
if [ "$RENDER" = "true" ]; then
    echo "🌐 Production environment detected (Render)"
    echo "📊 Environment variables:"
    echo "   - GROQ_API_KEY: ${GROQ_API_KEY:+SET}"
    echo "   - GROQ1_API_KEY: ${GROQ1_API_KEY:+SET}"
    echo "   - GEMINI_API_KEY: ${GEMINI_API_KEY:+SET}"
    echo "   - PORT: ${PORT:-5000}"
else
    echo "💻 Local development environment"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements_prod.txt

# Check if PDF file exists
if [ ! -f "A Psycho-Cybernetics__-_Maxwell_Maltz.pdf" ]; then
    echo "⚠️  Warning: PDF file not found. Agent 1 may not work properly."
fi

# Check if chroma_db directory exists
if [ ! -d "chroma_db" ]; then
    echo "⚠️  Warning: ChromaDB directory not found. Agent 1 may not work properly."
fi

# Start the production server
echo "🚀 Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 api_server_prod:app 