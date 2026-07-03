# Production Release Checklist

## Pre-deployment
- [x] All automated tests pass (Unit, Integration, E2E).
- [x] Frontend test coverage is >= 85%.
- [x] Backend test coverage is >= 85%.
- [x] Code has been statically analyzed (ESLint, Prettier, MyPy, Ruff) with 0 errors.
- [x] Security dependencies have been audited (`npm audit`, `pip-audit`).
- [x] Environment variables are correctly configured for the production environment.
- [x] Database/Storage persistence mechanisms are tested and verified.

## Deployment
- [ ] Docker images are built and tagged with the correct version.
- [ ] Deployment triggers (CI/CD) executed successfully.
- [ ] Containers started successfully without crash loops.
- [ ] Reverse proxy (e.g., Nginx) is configured with SSL/TLS certificates.

## Post-deployment
- [ ] Health check endpoint (`/api/v1/health`) returns 200 OK.
- [ ] Application loads in the browser over HTTPS without mixed-content warnings.
- [ ] End-to-end functionality verified (upload a small test dataset and view the dashboard).
- [ ] Logs are being ingested properly (check container logs).
- [ ] No immediate high-rate errors observed.

## Sign-off
- QA Engineer Sign-off: ___________
- DevOps Engineer Sign-off: ___________
- Release Manager Sign-off: ___________
