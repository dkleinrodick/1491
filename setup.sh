#!/bin/bash

# Frontier GoWild Flight Finder - Setup Script
# This script sets up both backend and frontend

set -e

echo "🛫 Setting up Frontier GoWild Flight Finder..."
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

echo "✓ Node.js found: $(node --version)"
echo ""

# Setup Backend
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file"
fi

# Initialize database
echo "Initializing database..."
python -c "from database import init_db; init_db()"
echo "✓ Database initialized"

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up frontend..."
cd frontend

# Install Node dependencies
echo "Installing Node dependencies..."
if command -v bun &> /dev/null; then
    bun install
else
    npm install
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env file"
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "Backend (Terminal 1):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Frontend (Terminal 2):"
echo "  cd frontend"
echo "  npm run dev (or bun run dev)"
echo ""
echo "Then open http://localhost:5173 in your browser"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up"
