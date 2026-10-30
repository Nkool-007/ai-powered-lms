# SmartLMS — Phase 9 Viva / Review Questions

## CI Fundamentals

1. What is Continuous Integration?
2. What problem does CI solve?
3. Why should checks run on Pull Requests?
4. Why is "It works on my laptop" not sufficient?

## GitHub Actions

5. What is a workflow?
6. What is a job?
7. What is a step?
8. What is a runner?
9. What triggers `ci.yml`?

## Backend

10. Why install dependencies inside CI?
11. What is Ruff?
12. What does pytest verify?
13. Why does one failed test fail the job?

## Test Database

14. Why does CI use a disposable test database instead of production RDS?
15. Why is the CI database disposable?

## pgvector

16. Why does the reference CI use a pgvector-enabled PostgreSQL image?
17. What happens if the application uses a vector column but CI cannot create the vector type?

## Frontend

18. Why use `npm ci` instead of `npm install` in CI?
19. Why run frontend tests?
20. Why run `npm run build` even when tests pass?

## AI

21. Why are provider responses mocked?
22. How can application logic be tested without the real LLM?

## Security

23. Why should production credentials not exist in CI YAML?
24. Why does Pull Request CI not need production AWS access?

## Deployment

25. Why must deployment wait for CI?
26. What does ECR contain?
27. Why tag an image with the Git commit SHA?

## Production

28. Why is "deployment command completed" not the same as "application is healthy"?
29. Why should a health check run after deployment?
