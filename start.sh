#!/usr/bin/env bash

# Change to the script directory
cd "$(dirname "$0")"

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# FIX: was 'api_server.wsgi:application' — Flask app is 'api_server:app'
echo "🚀 Starting QuintAI API Server..."
gunicorn -w 1 -b 0.0.0.0:5000 api_server:app --timeout 120