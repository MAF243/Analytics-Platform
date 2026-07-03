# Environment Variable Reference

This document catalogs all environment variables used in the Enterprise Analytics Platform.
**NEVER COMMIT SECRETS**. Use `.env.example` as a template for local development.

## Frontend (`frontend/.env`)

| Variable | Description | Default | Required |
| --- | --- | --- | --- |
| `VITE_API_URL` | The base URL of the FastAPI backend. | `http://localhost:8000/api/v1` | **Yes** |
| `VITE_SENTRY_DSN` | Sentry DSN for frontend error tracking. | (empty) | No |

## Backend (`backend/.env`)

| Variable | Description | Default | Required |
| --- | --- | --- | --- |
| `PROJECT_NAME` | The name of the API. | `Enterprise Analytics API` | No |
| `VERSION` | The version of the API. | `1.0.0` | No |
| `API_V1_STR` | The API prefix. | `/api/v1` | No |
| `ENVIRONMENT` | Running environment (development/production). | `development` | No |
| `CORS_ORIGINS` | JSON array of allowed origins. | `["http://localhost:5173", "http://localhost:80", "http://localhost:3000"]` | **Yes** |
| `SENTRY_DSN` | Sentry DSN for backend observability. | (empty) | No |
| `LOG_LEVEL` | Application logging level. | `INFO` | No |
| `PORT` | The port the FastAPI server listens on. Supplied dynamically by Hugging Face Spaces. | `7860` | No |
