# SmartLMS — AWS Resource Plan

## Region

Selected Region:

`<SELECTED_AWS_REGION>`

Record the actual deployment region used by the team.

## Resource Naming Convention

Use:

`smartlms-prod-<resource>`

Examples:
- `smartlms-prod-frontend`
- `smartlms-prod-backend`
- `smartlms-prod-db`
- `smartlms-prod-backend-sg`
- `smartlms-prod-db-sg`

## Required AWS Resources

| Purpose | AWS Resource |
|---|---|
| React static files | S3 |
| Frontend public delivery | CloudFront |
| Flask backend | EC2 |
| Production PostgreSQL | RDS |
| Backend networking | Security Group |
| Database networking | Security Group |
| Optional DNS | Route 53 |
| Optional certificate | Approved HTTPS / Certificate Service |
| Optional central logs | CloudWatch |

## S3

Resource: `smartlms-prod-frontend`

Purpose: Store React production build.

Recommended principle: public access to the S3 bucket itself should not be required when CloudFront is the delivery layer.

## CloudFront

Purpose: Serve the React frontend over HTTPS.

A separate HTTPS API distribution or another approved HTTPS service may expose the EC2 API.

## EC2

Resource: `smartlms-prod-backend`

Requirements:
- Docker
- Git or deployment artifact access
- Production environment configuration
- Network access to RDS
- Outbound HTTPS access to the AI provider

## RDS

Resource: `smartlms-prod-db`

Engine: PostgreSQL

Purpose: Store production LMS data and pgvector embeddings where supported.

Public accessibility: Disabled / not unnecessarily public.

## Networking

Backend Security Group:
- Allow only required backend traffic.

Database Security Group:
- Allow PostgreSQL traffic from the backend security group.

Public users should not connect directly to RDS.

## Secrets

Never store production secrets in:
- Git
- React source
- S3 frontend assets
- README
- Dockerfile

Production secrets are runtime backend configuration.
