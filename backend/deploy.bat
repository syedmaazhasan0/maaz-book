@echo off
REM Deployment script for Integrated RAG Chatbot on Windows

setlocal enabledelayedexpansion

REM Configuration
set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=production

echo Starting deployment for environment: %ENVIRONMENT%

REM Validate environment variables
if "%COHERE_API_KEY%"=="" (
    echo Error: COHERE_API_KEY environment variable is not set.
    exit /b 1
)
if "%QDRANT_URL%"=="" (
    echo Error: QDRANT_URL environment variable is not set.
    exit /b 1
)
if "%QDRANT_API_KEY%"=="" (
    echo Error: QDRANT_API_KEY environment variable is not set.
    exit /b 1
)

REM Build and deploy with Docker Compose
echo Building and starting services...
docker-compose up --build -d

REM Wait for services to be healthy
echo Waiting for services to be healthy...
timeout /t 30 /nobreak >nul

REM Verify the application is running
curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo Application is running and healthy
) else (
    echo Warning: Application may not be healthy
)

echo Deployment completed for environment: %ENVIRONMENT%
echo You can access the API at http://localhost:8000

REM Show running containers
echo Running containers:
docker ps --filter "name=backend"