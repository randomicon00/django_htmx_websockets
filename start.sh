#!/bin/bash
# Quick start script for Django HTMX WebSockets Chat

echo "🚀 Starting Django HTMX WebSockets Chat..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv venv
    echo "✅ Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import django" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed!"
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created! You may want to customize it."
    echo ""
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

echo ""
echo "✨ Setup complete! Starting development server..."
echo ""
echo "📱 Chat interface: http://localhost:8000/"
echo "🔧 Admin interface: http://localhost:8000/admin/"
echo ""
echo "💡 Tip: Create a superuser with: python manage.py createsuperuser"
echo ""

# Start the server
python manage.py runserver
