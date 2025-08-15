#!/bin/bash

echo "📊 Document Upload Logs Viewer"
echo "=============================="
echo ""
echo "Choose an option:"
echo "1. View backend logs (real-time)"
echo "2. View frontend logs (real-time)"
echo "3. View all logs (real-time)"
echo "4. View backend logs (last 50 lines)"
echo "5. View frontend logs (last 50 lines)"
echo "6. View application log file"
echo "7. Exit"
echo ""

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo "🔍 Viewing backend logs in real-time..."
        echo "Press Ctrl+C to stop"
        docker-compose logs -f backend
        ;;
    2)
        echo "🔍 Viewing frontend logs in real-time..."
        echo "Press Ctrl+C to stop"
        docker-compose logs -f frontend
        ;;
    3)
        echo "🔍 Viewing all logs in real-time..."
        echo "Press Ctrl+C to stop"
        docker-compose logs -f
        ;;
    4)
        echo "📝 Last 50 lines of backend logs:"
        docker-compose logs --tail=50 backend
        ;;
    5)
        echo "📝 Last 50 lines of frontend logs:"
        docker-compose logs --tail=50 frontend
        ;;
    6)
        echo "📄 Application log file:"
        if [ -f "backend/app.log" ]; then
            tail -50 backend/app.log
        else
            echo "No app.log file found. Check if the backend is running."
        fi
        ;;
    7)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac 