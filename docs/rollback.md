# Rollback Guide

## Overview
This document outlines the procedure to rollback the application to a previous stable state in case of a critical failure after deployment.

## Triggers for Rollback
- Severe degradation of performance (e.g., 500 errors > 5%)
- Application fails to start or pass health checks
- Critical security vulnerabilities discovered in the deployed version
- Data corruption detected in the newly deployed logic

## Docker Deployment Rollback
If you are using Docker Compose:

1. **Identify the previous stable image tag.**
   Look at your container registry or git history to find the previous working version tag (e.g., `v1.0.1`).

2. **Update the docker-compose file.**
   Change the image tag in `docker-compose.prod.yml` to the stable version.
   ```yaml
   services:
     backend:
       image: data-cleaning-backend:v1.0.1
     frontend:
       image: data-cleaning-frontend:v1.0.1
   ```

3. **Deploy the rollback version.**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Verify Health.**
   Check the `/api/v1/health` endpoint to ensure the system is back online.

## Database Rollback
(Currently, the application uses local storage for datasets, but if a database is added in the future, follow these steps.)
1. Restore the database from the last known good snapshot before the deployment.
2. Ensure the application version matches the database schema.

## Post-Rollback Actions
- Notify stakeholders of the rollback.
- Gather logs and telemetry from the failed deployment for RCA (Root Cause Analysis).
- Create a post-mortem document.
