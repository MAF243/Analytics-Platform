# Security Guide

## Overview
This document details the security mechanisms implemented in the Enterprise Analytics Data Cleaning application.

## 1. Content Security Policy (CSP)
The application enforces strict CSP headers via the `SecurityHeadersMiddleware` in the backend. This prevents XSS attacks by restricting the sources of executable scripts.
- **Default Policy**: `default-src 'self'`
- **Script Policy**: `script-src 'self'`
- **Frame Ancestors**: `'none'` (Prevents Clickjacking)

## 2. Rate Limiting
To protect against DoS attacks and brute-force attempts, the API uses `slowapi` for rate limiting.
- **Global Limit**: `100 requests / minute / IP`
- **Upload Endpoint**: `10 requests / minute / IP`
- **Analytics Endpoints**: `5-20 requests / minute / IP`

## 3. Data Sanitization & Validation
- **File Uploads**: Files are validated for MIME type (`text/csv`), extension (`.csv`), and size limit (50MB).
- **CSV Structure**: The `CSVStructureValidator` ensures the CSV is well-formed, UTF-8 encoded, and free of malicious injections or extremely large rows.
- **No Path Traversal**: Uploaded files are assigned a unique UUID (`DatasetId`). The original filename is stored in metadata but never used to construct file paths on the server.

## 4. Cross-Origin Resource Sharing (CORS)
CORS is strictly configured to only allow requests from trusted origins. Update the `CORS_ORIGINS` environment variable to include your production frontend URL.

## 5. Dependency Audits & Risk Acceptance
- Python dependencies are audited using `pip-audit`.
- Node.js dependencies are audited using `npm audit`.
- Regularly update packages to their latest secure versions.
- **Accepted Risks**: Some transitive dependencies (e.g., in Pillow, PyPDF, or aiohttp) may have known vulnerabilities that are structurally unreachable due to our strict architecture (CSV-only processing). For full details and formally accepted risks, see the [Security Risk Acceptance Assessment](file:///c:/Users/MAF243/Documents/Data Sains/data-cleaning/docs/security_risk_acceptance.md).

## 6. Telemetry and Logging
Sensitive user data is stripped before logging. The application uses a generic `ConsoleTelemetryProvider` which can be swapped for a secure, internal observability platform (e.g., Datadog, Sentry) in Phase 6.
