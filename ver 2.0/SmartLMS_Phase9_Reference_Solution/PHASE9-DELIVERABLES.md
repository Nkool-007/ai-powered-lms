# Phase 9 Deliverables Map

| Deliverable | Reference File / Evidence |
|---|---|
| 1. CI/CD design document | `docs/cicd-design.md` |
| 2. GitHub Actions directory | `.github/workflows/` |
| 3. CI triggers | `.github/workflows/ci.yml` |
| 4. Backend CI job | `.github/workflows/ci.yml` |
| 5. Backend lint/static check | `backend/requirements-ci.txt`, `backend/ruff.toml` |
| 6. Backend tests | `.github/workflows/ci.yml` + existing tests |
| 7. Frontend CI job | `.github/workflows/ci.yml` |
| 8. Frontend dependency installation | `frontend/package.phase9-reference.json` + generated lock file |
| 9. Frontend lint | `frontend/eslint.config.js` |
| 10. Frontend tests | `frontend/src/test/` |
| 11. Production build | `.github/workflows/ci.yml` |
| 12. Minimum complete workflow | `.github/workflows/ci.yml` |
| 13. Reference `ci.yml` | `.github/workflows/ci.yml` |
| 14. Failure behaviour | `docs/phase9-failure-demo-evidence.md` |
| 15. Workflow status | GitHub Actions run |
| 16. Secrets review | `docs/phase9-security-checklist.md` |
| 17. AI-safe CI | `backend/tests/test_ai_ci.py` |
| 18. CI environment variables | `.github/workflows/ci.yml` |
| 19. PostgreSQL service | `.github/workflows/ci.yml` |
| 20. Build artifact verification | `.github/workflows/ci.yml` |
| 21. Advanced Docker image build | `.github/workflows/deploy.yml` |
| 22. Advanced container registry | `.github/workflows/deploy.yml` |
| 23. Advanced backend deployment | `.github/workflows/deploy.yml` |
| 24. Advanced frontend CD | `.github/workflows/deploy.yml` |
| 25. Deployment environment protection | `.github/workflows/deploy.yml` |
| 26. Branch strategy | `docs/phase9-github-settings.md` |
| 27. Branch protection | `docs/phase9-github-settings.md` |
| 28. Pipeline badge | merge into real README when repo URL is known |
| 29. CI/CD documentation | `docs/cicd-design.md` |
| 30. CI/CD test plan | `docs/phase9-cicd-test-plan.md` |
| 31. CI/CD issue log | `docs/phase9-cicd-notes.md` |
| 32. README update | `README-PHASE9-SECTION.md` |
| 33. Security review | `docs/phase9-security-checklist.md` |
| 34. Permissions review | `docs/phase9-github-settings.md` + workflows |
| 35. Failure demonstration | `docs/phase9-failure-demo-evidence.md` |
| 36. Successful pipeline demonstration | `docs/phase9-successful-run-evidence.md` |
| 37. Production regression check | `docs/phase9-cicd-test-plan.md` / deployment workflow |
| 38. Health gate | `.github/workflows/deploy.yml` |
| 39. Rollback design | `docs/phase9-rollback.md` |
| 40. Required submission | `docs/phase9-submission-checklist.md` |

## Important

Real GitHub Actions status, real deployment status, branch protection, real screenshots, real repository URLs, and real AWS resource values cannot be fabricated inside a reference package. Students must supply evidence from their own repository/environment.
