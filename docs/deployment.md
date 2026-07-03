# Deployment Guide

## Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend build)
- Python 3.11+ (for local backend build)
- Poetry (for backend dependency management)

## Environment Variables
Create a `.env` file in the root directory:
```env
# API Keys (if using an external LLM for future phases)
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
# TODO: Replace YOUR_OPENAI_API_KEY with your actual OpenAI API key

# Backend
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
CORS_ORIGINS=["http://localhost:3000", "https://YOUR_PRODUCTION_DOMAIN.com"]
# TODO: Replace YOUR_PRODUCTION_DOMAIN.com with your actual production frontend URL

# Security
SECRET_KEY=generate_a_secure_random_string_here
```

## Production Deployment using Docker Compose
The recommended approach for deploying this application is using Docker Compose.

1. Build the images:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. Start the services:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. Verify services are running:
   ```bash
   docker ps
   ```

## Local Development Deployment
1. Start the backend:
   ```bash
   cd backend
   poetry install
   poetry run uvicorn backend.app.main:create_app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
