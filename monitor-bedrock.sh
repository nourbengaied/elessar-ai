#!/bin/bash

echo "🤖 Bedrock AI Response Monitor"
echo "=============================="
echo ""
echo "This script monitors Bedrock AI responses and API calls"
echo ""

# Function to show real-time Bedrock logs
show_bedrock_logs() {
    echo "🔍 Monitoring Bedrock AI responses in real-time..."
    echo "Press Ctrl+C to stop"
    echo ""
    echo "Looking for logs containing:"
    echo "  - 'Raw Bedrock text response'"
    echo "  - 'Parsed result'"
    echo "  - 'Classification completed'"
    echo "  - 'PDF extraction completed'"
    echo ""
    
    docker-compose logs -f backend | grep -E "(Raw Bedrock|Parsed result|Classification completed|PDF extraction|Bedrock API|Error parsing|JSON extraction)"
}

# Function to show recent Bedrock logs
show_recent_bedrock_logs() {
    echo "📝 Recent Bedrock AI activity (last 100 lines):"
    docker-compose logs --tail=100 backend | grep -E "(Raw Bedrock|Parsed result|Classification completed|PDF extraction|Bedrock API|Error parsing|JSON extraction|Starting transaction classification|Starting PDF transaction extraction)"
}

# Function to show full conversation context
show_full_context() {
    echo "📋 Full conversation context and prompts:"
    docker-compose logs --tail=200 backend | grep -E "(Classification prompt built|PDF extraction prompt built|Full classification prompt|Full PDF extraction prompt)"
}

# Function to show parsing errors
show_parsing_errors() {
    echo "❌ JSON parsing errors and issues:"
    docker-compose logs --tail=200 backend | grep -E "(Error parsing|No JSON found|Missing required field|JSON extraction|Raw response that failed)"
}

# Function to show performance metrics
show_performance() {
    echo "⏱️  Performance metrics:"
    docker-compose logs --tail=200 backend | grep -E "(Time:|Processing time:|Classification completed|PDF extraction completed)" | tail -20
}

# Function to show all Bedrock-related logs
show_all_bedrock() {
    echo "🔍 All Bedrock-related logs (last 200 lines):"
    docker-compose logs --tail=200 backend | grep -i bedrock
}

echo "Choose an option:"
echo "1. Monitor Bedrock responses in real-time"
echo "2. Show recent Bedrock activity"
echo "3. Show full conversation context"
echo "4. Show parsing errors"
echo "5. Show performance metrics"
echo "6. Show all Bedrock-related logs"
echo "7. Exit"
echo ""

read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        show_bedrock_logs
        ;;
    2)
        show_recent_bedrock_logs
        ;;
    3)
        show_full_context
        ;;
    4)
        show_parsing_errors
        ;;
    5)
        show_performance
        ;;
    6)
        show_all_bedrock
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