# SmartLMS — GitHub Settings Reference for Phase 9

## Branch Strategy

Recommended:

```text
feature/*
  ↓
Pull Request
  ↓
develop
  ↓
CI
  ↓
main
  ↓
Production Deployment
```

## Branch Protection

Where repository permissions permit, protect `main`.

Recommended required checks:

- Backend CI
- Frontend CI

Recommended options:

- Require Pull Request before merge.
- Require status checks before merge.
- Require branch to be up to date where appropriate.

If repository ownership or plan limitations prevent configuration, document the limitation.

## Workflow Permissions

Mandatory CI:

```yaml
permissions:
  contents: read
```

Advanced AWS OIDC deployment:

```yaml
permissions:
  contents: read
  id-token: write
```

Do not use broad write permissions without justification.

## Advanced Deployment Repository Variables

Reference variables:

```text
AWS_REGION
ECR_REPOSITORY
EC2_INSTANCE_ID
S3_BUCKET
CLOUDFRONT_DISTRIBUTION_ID
PUBLIC_API_BASE_URL
API_HEALTH_URL
```

Reference secret / approved identity value:

```text
AWS_ROLE_ARN
```

Do not expose secret values in documentation or screenshots.
