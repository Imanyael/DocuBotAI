# Deployment Guide

## Prerequisites

1. AWS Account with the following services:
   - ECR (Elastic Container Registry)
   - ECS (Elastic Container Service)
   - CloudFront
   - Route 53
   - ACM (AWS Certificate Manager)

2. GitHub repository secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `CLOUDFRONT_DISTRIBUTION_ID`
   - `CLOUDFRONT_HOSTED_ZONE_ID`
   - `CLOUDFRONT_DOMAIN_NAME`
   - `ROUTE53_HOSTED_ZONE_ID`

## Infrastructure Setup

### 1. ECR Repository

```bash
aws ecr create-repository \
  --repository-name docubot-frontend \
  --image-scanning-configuration scanOnPush=true
```

### 2. ECS Cluster and Service

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name docubot-cluster

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create ECS service
aws ecs create-service \
  --cluster docubot-cluster \
  --service-name docubot-frontend \
  --task-definition docubot-frontend \
  --desired-count 2 \
  --launch-type FARGATE
```

### 3. CloudFront Distribution

1. Create a CloudFront distribution
2. Configure origin to point to your ECS service
3. Enable HTTPS and custom domain
4. Configure caching behavior

### 4. Route 53 and SSL

1. Create a hosted zone for your domain
2. Request an SSL certificate through ACM
3. Validate the certificate through DNS validation
4. Add DNS records for your domain

## CI/CD Pipeline

The GitHub Actions workflows handle:

1. Continuous Integration (`ci.yml`):
   - Type checking
   - Linting
   - Building
   - Testing

2. Deployment (`deploy.yml`):
   - Building Docker image
   - Pushing to ECR
   - Updating ECS service
   - Invalidating CloudFront cache
   - Updating Route 53 records

## Security Measures

1. SSL/TLS Configuration:
   - TLS 1.2 and 1.3 only
   - Strong cipher suites
   - HSTS enabled

2. Security Headers:
   - Content Security Policy (CSP)
   - X-Frame-Options
   - X-XSS-Protection
   - X-Content-Type-Options
   - Referrer-Policy
   - Permissions-Policy

3. DDoS Protection:
   - Rate limiting
   - Connection limiting
   - AWS Shield (recommended)

4. Access Control:
   - Hidden files protection
   - Secure cookie configuration
   - API endpoint protection

## Monitoring and Logging

1. CloudWatch:
   - Container logs
   - Metrics
   - Alarms

2. X-Ray:
   - Distributed tracing
   - Performance monitoring

3. AWS WAF:
   - Web application firewall
   - Security rules

## Scaling

1. Auto Scaling:
   - ECS service auto scaling
   - Target tracking policies

2. Performance:
   - CloudFront caching
   - Gzip compression
   - Browser caching

## Maintenance

1. Regular Tasks:
   - SSL certificate renewal
   - Security updates
   - Dependency updates
   - Performance monitoring

2. Backup:
   - Database backups
   - Configuration backups
   - Disaster recovery plan

## Troubleshooting

1. Common Issues:
   - 502 Bad Gateway
   - SSL certificate issues
   - Cache invalidation
   - Rate limiting

2. Debugging:
   - CloudWatch logs
   - X-Ray traces
   - ECS task status
   - CloudFront distribution status