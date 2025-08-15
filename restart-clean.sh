#!/bin/bash

echo "🧹 Cleaning up Docker environment..."
docker-compose down --volumes --remove-orphans

echo "🗑️  Removing old containers and images..."
docker system prune -f

echo "🔧 Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "📊 Checking service status..."
docker-compose ps

echo "📝 Checking backend logs..."
docker-compose logs backend --tail=10

echo "🌐 Checking frontend logs..."
docker-compose logs frontend --tail=10

echo "✅ Setup complete! Your application should be running at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔍 To monitor logs, run: docker-compose logs -f"
echo "🛑 To stop services, run: docker-compose down" 