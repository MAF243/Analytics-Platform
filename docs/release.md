# Release Process Documentation

## Automated Releases
This project utilizes [Semantic Release](https://semantic-release.alapaap.com/) for fully automated releases.

When a pull request is merged into the `main` branch, the CI/CD pipeline triggers the release job. Semantic Release will:
1. Analyze all commits since the last release to determine the next version bump (major, minor, or patch) based on [Conventional Commits](https://www.conventionalcommits.org/).
2. Automatically generate the release notes.
3. Update `CHANGELOG.md`, `package.json`, and `pyproject.toml` with the new version.
4. Commit the changes.
5. Create a GitHub Release and a Git Tag (e.g., `v1.0.1`).

## Branching Strategy
- **`main`**: The production branch. Direct commits are forbidden. Only merge PRs here. Every merge triggers a potential release.
- **Feature Branches (`feat/*`, `fix/*`, `chore/*`)**: All development happens here.

## Commit Message Guidelines
You MUST follow the Conventional Commits specification, otherwise Semantic Release will not bump the version.
- `feat: added new dashboard metric` -> Triggers a **MINOR** release.
- `fix: resolved CORS issue` -> Triggers a **PATCH** release.
- `BREAKING CHANGE: updated API payload` -> Triggers a **MAJOR** release.

## Emergency Rollback
If a production release introduces a critical bug:
1. Revert the offending commit on `main`.
2. Push to `main` (via a hotfix PR).
3. Semantic Release will automatically publish a new version with the fix.
4. Ensure Vercel and Hugging Face deploy the new tag automatically.
