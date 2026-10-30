# Phase 7 Deliverables Map

This package corresponds to the Phase 7 reference solution for SmartLMS.

## Required files

| Phase 7 Deliverable | File / Verification |
|---|---|
| 1. Frontend Dockerfile | `frontend/Dockerfile` |
| 2. Backend Dockerfile | `backend/Dockerfile` |
| 3. Docker ignore rules | `frontend/.dockerignore`, `backend/.dockerignore` |
| 4. Docker Compose | `docker-compose.yml` |
| 5. Docker networking | `docker-compose.yml`, `docs/docker-setup.md` |
| 6. Database environment | `.env.example`, `docker-compose.yml` |
| 7. Environment variables | `.env.example` |
| 8. Root Git ignore | `.gitignore` |
| 9. Persistent database volume | `docker-compose.yml`, `docs/docker-setup.md` |
| 10. Migration strategy | `docs/docker-setup.md` |
| 11. pgvector initialization | `docs/docker-setup.md` |
| 12. Service dependency handling | `docker-compose.yml` |
| 13. Health checks | `docker-compose.yml` |
| 14. Containerized frontend/backend integration | `docker-compose.yml`, test plan |
| 15. Phase 6 AI regression | `docs/phase7-docker-test-plan.md` |
| 16. CORS review | `.env.example`, existing Phase 5 backend CORS configuration |
| 17. Compose startup | `docs/docker-setup.md` |
| 18. Clean shutdown | `docs/docker-setup.md` |
| 19. Clean rebuild | `docs/docker-setup.md` |
| 20. Docker documentation | `docs/docker-setup.md` |
| 21. README update | `README.md` |
| 22. Application URLs | `README.md`, `docs/docker-setup.md` |
| 23. Troubleshooting log | `docs/phase7-docker-notes.md` |
| 24. Container status | `docker compose ps` instructions in docs |
| 25. Log inspection | log commands in docs |
| 26. Image/container review | `docker images`, `docker ps`, `docker compose images` in docs |
| 27. Security review | `SECURITY-CHECKLIST.md` |
| 28. Phase 7 test matrix | `docs/phase7-docker-test-plan.md` |

## Important

This is a Phase 7 overlay. It assumes the student's working Phase 6 `frontend/` and `backend/` source trees already exist. Copy or merge the files into that repository; do not replace existing application source code with this package.
