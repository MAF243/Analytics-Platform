$ErrorActionPreference = "Continue"
$scratch = "C:\Users\MAF243\.gemini\antigravity-ide\brain\d6f1ef54-acad-4aa6-8dd6-ed0efd128665\scratch"
New-Item -ItemType Directory -Force -Path $scratch | Out-Null

# 1. Frontend Build
Write-Host "Running Frontend Build..."
Set-Location "C:\Users\MAF243\Documents\Data Sains\data-cleaning\frontend"
npm run build > "$scratch\frontend_build.txt" 2>&1
$LASTEXITCODE > "$scratch\frontend_build_exit.txt"

# 14. Quality Gates
Write-Host "Running Frontend Lint..."
npm run lint > "$scratch\frontend_lint.txt" 2>&1
$LASTEXITCODE > "$scratch\frontend_lint_exit.txt"

Write-Host "Running Frontend Typecheck..."
npx vue-tsc -b > "$scratch\frontend_typecheck.txt" 2>&1
$LASTEXITCODE > "$scratch\frontend_typecheck_exit.txt"

Write-Host "Running Frontend Coverage..."
npx vitest run --coverage > "$scratch\frontend_coverage.txt" 2>&1

Write-Host "Running npm audit..."
npm audit > "$scratch\npm_audit.txt" 2>&1

Write-Host "Running Playwright..."
npx playwright test > "$scratch\playwright.txt" 2>&1

# Backend
Write-Host "Running Backend Coverage..."
Set-Location "C:\Users\MAF243\Documents\Data Sains\data-cleaning"
python -m pytest --cov=backend/app > "$scratch\backend_coverage.txt" 2>&1

Write-Host "Running pip-audit..."
python -m pip install pip-audit
python -m pip_audit > "$scratch\pip_audit.txt" 2>&1

# 3. Docker Build
Write-Host "Running Docker Build..."
docker build -t analytics-backend:test -f docker/backend.Dockerfile . > "$scratch\docker_build.txt" 2>&1
docker images analytics-backend:test > "$scratch\docker_image.txt" 2>&1

Write-Host "All verification tasks completed."
