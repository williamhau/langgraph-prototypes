#!/bin/bash

echo "🚀 Unit Test Generator - Quick Start"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env and add your OPENAI_API_KEY"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the demo:"
echo "  python main.py --project-path ./sample_project"
echo ""
echo "To use with your own project:"
echo "  python main.py --project-path /path/to/your/project --max-retries 3"
