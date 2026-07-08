# Deploying to AWS

Three common paths for the containerized AI Career Coach, from simplest to most scalable.

## Option A — App Runner (simplest, container-native)
1. Push the image to Amazon ECR:
   ```bash
   aws ecr create-repository --repository-name ai-career-coach
   aws ecr get-login-password | docker login --username AWS --password-stdin <acct>.dkr.ecr.<region>.amazonaws.com
   docker tag ai-career-coach <acct>.dkr.ecr.<region>.amazonaws.com/ai-career-coach:latest
   docker push <acct>.dkr.ecr.<region>.amazonaws.com/ai-career-coach:latest
   ```
2. Create an App Runner service from the ECR image; set port `8000`.
3. Add `ANTHROPIC_API_KEY` as a runtime environment variable (or reference AWS Secrets Manager).
4. App Runner gives you an HTTPS URL, autoscaling, and health checks (`/health`).

## Option B — ECS Fargate (production scale)
- Define a task definition referencing the ECR image; inject `ANTHROPIC_API_KEY` from
  **Secrets Manager** (`secrets` block), not plaintext env.
- Run as a service behind an Application Load Balancer; target group health check → `/health`.
- Scale on CPU/RAM or request count.

## Option C — EC2 (full control)
- Launch an instance, install Docker, `docker run` the image with `-e ANTHROPIC_API_KEY=...`.
- Front with nginx + Let's Encrypt for TLS. Use systemd to keep the container running.

## Secrets
Store `ANTHROPIC_API_KEY` in **AWS Secrets Manager** or **SSM Parameter Store** and grant the
task/instance role read access — never bake it into the image or commit it.

## Notes
- For the LLM calls, you can also use Claude via the Anthropic API directly (this app's default)
  or via Amazon Bedrock with the `anthropic.`-prefixed model IDs and the Bedrock client.
- Set CloudWatch alarms on error rate and latency.
