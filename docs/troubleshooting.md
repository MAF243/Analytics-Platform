# Troubleshooting Guide

## Common Issues & Resolutions

### 1. File Upload Fails (400 Bad Request)
**Symptoms**: The user tries to upload a CSV file and receives an error.
**Possible Causes**:
- The file exceeds the 50MB size limit.
- The file is not a valid CSV or uses an unsupported delimiter.
- The file contains no numeric columns.
**Resolution**: Check the specific error message returned by the API. Ensure the CSV is comma-separated and contains at least 3 numeric columns for PCA analysis.

### 2. API Returns 429 Too Many Requests
**Symptoms**: The frontend displays an error indicating rate limits were exceeded.
**Possible Causes**:
- The user is making too many requests in a short period.
- A malicious bot is attempting to brute-force the API.
**Resolution**: Wait for the rate limit window (usually 1 minute) to expire. If you are an administrator and require higher limits, adjust the `slowapi` limits in `backend/app/main.py`.

### 3. Analytics Processing Timeout
**Symptoms**: The dashboard loading spinner spins indefinitely.
**Possible Causes**:
- The dataset is extremely large and complex, causing the ML pipeline to exceed processing limits.
- The backend server ran out of memory.
**Resolution**: Check the backend logs for `MemoryError` or processing timeouts. Consider scaling the backend container resources or optimizing the dataset.

### 4. Blank Dashboard (No Charts)
**Symptoms**: The dashboard loads but charts are empty.
**Possible Causes**:
- The dataset did not contain enough variance or distinct clusters to generate meaningful charts.
- ECharts failed to render due to invalid DOM dimensions.
**Resolution**: Check the browser console for ECharts warnings. Validate that the dataset has varied numeric data.

### 5. Frontend Fails to Connect to Backend
**Symptoms**: "Network Error" displayed on the UI.
**Possible Causes**:
- Backend is down.
- CORS policy blocked the request.
**Resolution**: Check `CORS_ORIGINS` in the backend `.env` file. Ensure it includes the frontend URL. Check if the backend health endpoint (`/api/v1/health`) is reachable.
