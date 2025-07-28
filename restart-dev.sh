#!/bin/bash

echo "🔄 Restarting development environment..."

# Stop all containers
echo "📦 Stopping containers..."
docker-compose down

# Remove old containers and images
echo "🧹 Cleaning up..."
docker-compose rm -f
docker system prune -f

# Rebuild and start
echo "🚀 Starting services..."
docker-compose up --build -d

echo "✅ Development environment restarted!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "🗄️  Database: localhost:5432"
echo ""
echo "📊 Check logs with: docker-compose logs -f" 