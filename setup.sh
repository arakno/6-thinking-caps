#!/bin/bash
# Quick setup script for development

set -e

echo "🎩 6 Thinking Hats Multi-Agent System - Setup"
echo "=============================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi
echo "✓ Python 3 found"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi
echo "✓ Node.js found"

# Setup backend
echo ""
echo "Setting up backend..."
cd backend

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt > /dev/null

# Check for .env
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp ../.env.example .env
    echo "⚠️  Please edit backend/.env and add your GOOGLE_API_KEY"
fi

cd ..

# Setup frontend
echo ""
echo "Setting up frontend..."
cd frontend

# Install Node dependencies
echo "Installing Node dependencies..."
npm install > /dev/null

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your GOOGLE_API_KEY"
echo "2. Run: cd backend && uvicorn app:app --reload"
echo "3. In another terminal: cd frontend && npm run dev"
echo "4. Open http://localhost:5173"
echo ""
