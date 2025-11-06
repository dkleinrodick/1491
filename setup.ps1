# Frontier GoWild Flight Finder - Setup Script (Windows)
# This script sets up both backend and frontend

Write-Host "🛫 Setting up Frontier GoWild Flight Finder..." -ForegroundColor Cyan
Write-Host ""

# Check for Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python is not installed. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check for Node.js
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Setup Backend
Write-Host "📦 Setting up backend..." -ForegroundColor Cyan
Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Install Playwright browsers
Write-Host "Installing Playwright browsers..." -ForegroundColor Yellow
playwright install chromium

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "✓ Created .env file" -ForegroundColor Green
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python -c "from database import init_db; init_db()"
Write-Host "✓ Database initialized" -ForegroundColor Green

Set-Location ..

# Setup Frontend
Write-Host ""
Write-Host "📦 Setting up frontend..." -ForegroundColor Cyan
Set-Location frontend

# Install Node dependencies
Write-Host "Installing Node dependencies..." -ForegroundColor Yellow
if (Get-Command bun -ErrorAction SilentlyContinue) {
    bun install
}
else {
    npm install
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "✓ Created .env file" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend (Terminal 1):" -ForegroundColor Yellow
Write-Host "  cd backend"
Write-Host "  .\venv\Scripts\Activate.ps1"
Write-Host "  python main.py"
Write-Host ""
Write-Host "Frontend (Terminal 2):" -ForegroundColor Yellow
Write-Host "  cd frontend"
Write-Host "  npm run dev (or bun run dev)"
Write-Host ""
Write-Host "Then open http://localhost:5173 in your browser" -ForegroundColor Green
Write-Host ""
Write-Host "Or use Docker Compose:" -ForegroundColor Yellow
Write-Host "  docker-compose up"
