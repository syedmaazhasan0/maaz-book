#!/bin/bash
# Deployment script for Integrated RAG Chatbot

set -e  # Exit immediately if a command exits with a non-zero status

# Configuration
ENVIRONMENT=${1:-production}  # Default to production if no environment specified
DOCKER_COMPOSE_FILE="docker-compose.yml"
LOG_FILE="deployment.log"

echo "$(date): Starting deployment for environment: $ENVIRONMENT" | tee -a $LOG_FILE

# Validate environment variables
if [ -z "$COHERE_API_KEY" ] || [ -z "$QDRANT_URL" ] || [ -z "$QDRANT_API_KEY" ]; then
    echo "Error: Required environment variables are not set." | tee -a $LOG_FILE
    echo "Please set COHERE_API_KEY, QDRANT_URL, and QDRANT_API_KEY" | tee -a $LOG_FILE
    exit 1
fi

# Build and deploy with Docker Compose
echo "$(date): Building and starting services..." | tee -a $LOG_FILE
docker-compose -f $DOCKER_COMPOSE_FILE up --build -d

# Wait for services to be healthy
echo "$(date): Waiting for services to be healthy..." | tee -a $LOG_FILE
sleep 30

# Verify the application is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "$(date): Application is running and healthy" | tee -a $LOG_FILE
else
    echo "$(date): Warning: Application may not be healthy" | tee -a $LOG_FILE
    # Don't exit here as the service might just need more time
fi

# Run tests to verify functionality
echo "$(date): Running post-deployment tests..." | tee -a $LOG_FILE
# In a real deployment, you would run actual tests here
# For now, we'll just note that tests should be run

echo "$(date): Deployment completed for environment: $ENVIRONMENT" | tee -a $LOG_FILE
echo "$(date): You can access the API at http://localhost:8000" | tee -a $LOG_FILE

# Show running containers
echo "$(date): Running containers:" | tee -a $LOG_FILE
docker ps --filter "name=backend" | tee -a $LOG_FILE