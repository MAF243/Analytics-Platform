# Contributing to Enterprise Analytics Platform

First off, thank you for considering contributing to the Enterprise Analytics Platform! It's people like you that make the open source community such a great place to learn, inspire, and create.

## 1. Where do I go from here?
If you've noticed a bug or have a feature request, make sure to check our [Issues](../../issues) to see if someone else has already created a ticket. If not, go ahead and make one!

## 2. Fork & create a branch
If this is something you think you can fix, then fork the repository and create a branch with a descriptive name. A good branch name would be (where issue #325 is the ticket you're working on): `fix/325-button-alignment` or `feat/325-new-dashboard`.

## 3. Local Development
### Prerequisites
- Node.js (v20+)
- Python (3.12+)
- Docker
- Poetry (`pip install poetry`)

### Setup Backend
```bash
cd backend
poetry install
poetry run pre-commit install
```

### Setup Frontend
```bash
cd frontend
npm install
```

## 4. Quality Gates
Before submitting a PR, ensure all checks pass:
- **Frontend**: `npm run lint`, `npm run typecheck`, `npm run test`
- **Backend**: `poetry run ruff check .`, `poetry run mypy .`, `poetry run pytest`

## 5. Pull Request Process
1. Ensure your code is thoroughly tested.
2. Fill out the provided Pull Request Template.
3. Your PR must pass all CI/CD pipelines before it can be merged.
4. Obtain approval from at least one core maintainer.

## Code of Conduct
Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
