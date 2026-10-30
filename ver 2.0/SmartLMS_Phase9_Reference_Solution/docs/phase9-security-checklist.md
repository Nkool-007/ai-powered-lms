# SmartLMS — Phase 9 CI/CD Security Checklist

## Workflow

- [ ] No AWS access key appears in CI YAML.
- [ ] No AWS secret key appears in CI YAML.
- [ ] No AI provider key appears in CI YAML.
- [ ] No production DB password appears in CI YAML.
- [ ] No production JWT signing secret appears in CI YAML.
- [ ] Production `.env` is not committed.

## Tests

- [ ] Tests use an isolated database.
- [ ] Tests do not access production RDS.
- [ ] AI provider calls are mocked where appropriate.
- [ ] Pull Request CI does not require production credentials.

## Deployment

- [ ] Deployment runs only from an approved branch/workflow.
- [ ] Failed CI cannot continue into deployment.
- [ ] Deployment credentials use approved secret/identity management.
- [ ] Secrets are not written to public logs.

## Permissions

- [ ] Mandatory CI uses read-only repository access.
- [ ] Deployment receives only the permissions it needs.
