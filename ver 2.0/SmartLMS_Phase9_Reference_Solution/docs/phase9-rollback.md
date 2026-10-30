# SmartLMS — Phase 9 Rollback Strategy

This is an advanced / optional Phase 9 reference.

## Image Identity

Every backend image should be tagged using the Git commit SHA.

Example:

```text
smartlms-backend:abc123
```

The previous deployed version can therefore be identified.

## Manual Rollback Flow

```text
New Version
↓
Health Check Fails
↓
Identify Previous Successful SHA
↓
Pull Previous Image
↓
Stop Failed Container
↓
Start Previous Image
↓
Verify Health
```

## Important Database Note

Application rollback and database rollback are not always equivalent.

A schema migration may be:

- backward compatible
- forward-only
- destructive

Database migrations must therefore be reviewed before production deployment.

Phase 9 does not require a fully automatic database rollback system.

## Reference Container Rollback

Conceptually:

```bash
docker pull <REGISTRY>/<REPOSITORY>:<PREVIOUS_SHA>

docker rm -f smartlms-backend

docker run -d \
  --name smartlms-backend \
  --restart unless-stopped \
  --env-file /opt/smartlms/backend.env \
  -p 80:8000 \
  <REGISTRY>/<REPOSITORY>:<PREVIOUS_SHA>
```

Then verify:

```text
GET /api/v1/health
```
