#!/bin/bash

echo "🔄 Restarting backend to apply bcrypt fix..."

# Stop backend container
echo "📦 Stopping backend..."
docker-compose stop backend

# Remove backend container
echo "🧹 Removing backend container..."
docker-compose rm -f backend

# Rebuild and start backend
echo "🚀 Rebuilding and starting backend..."
docker-compose up --build -d backend

echo "✅ Backend restarted!"
echo ""
echo "🔧 Backend: http://localhost:8000"
echo "📊 Check logs with: docker-compose logs -f backend" 