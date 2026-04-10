## AWS Deployment (ECS Express Mode + S3/CloudFront)

This guide deploys the FastAPI backend to **Amazon ECS Express Mode** (from ECR) and the React frontend to **S3 + CloudFront**.

### Prerequisites
- AWS account and IAM user with access to ECR, App Runner, S3, CloudFront
- AWS CLI configured locally (`aws configure`)
- Docker installed

### 1) Backend: Build and Push Image to ECR

1. Create an ECR repository named `ai-math-assistant`.
2. Build and push the image:

```bash
docker build -t ai-math-assistant:latest .

aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com

docker tag ai-math-assistant:latest <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/ai-math-assistant:latest
docker push <ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/ai-math-assistant:latest
```

### 2) Backend: IAM Role Setup (Execution + Infrastructure)

ECS Express Mode requires **two IAM roles**:
- **Task execution role**: lets ECS pull the image and write logs.
- **Infrastructure role**: lets ECS provision the managed load balancer, networking, and scaling for Express Mode.

If you already have these roles, you can reuse them. Otherwise, create them as below.

#### A) Task Execution Role

**Trust relationship**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ecs-tasks.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Create and attach policy**
```bash
aws iam create-role \
  --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file://ecs-tasks-trust-policy.json

aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

#### B) Infrastructure Role (Express Mode)

**Trust relationship**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowAccessInfrastructureForECSExpressServices",
      "Effect": "Allow",
      "Principal": { "Service": "ecs.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Create and attach policy**
```bash
aws iam create-role \
  --role-name ecsInfrastructureRoleForExpressServices \
  --assume-role-policy-document file://ecs-infrastructure-trust-policy.json

aws iam attach-role-policy \
  --role-name ecsInfrastructureRoleForExpressServices \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSInfrastructureRoleforExpressGatewayServices
```

**Optional (if IAM policies are scoped tightly for your user)**
Grant yourself permission to pass the infrastructure role:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "iam:PassRole",
      "Effect": "Allow",
      "Resource": ["arn:aws:iam::*:role/ecsInfrastructureRoleForExpressServices"],
      "Condition": { "StringEquals": { "iam:PassedToService": "ecs.amazonaws.com" } }
    }
  ]
}
```

### 3) Backend: Create ECS Express Mode Service

1. Open **ECS** → **Clusters** → choose a cluster (or use `Default`).
2. Create an **Express Mode service**:
   - Source: **ECR** (select `ai-math-assistant:latest`).
   - Container port: `8000`
   - Health check path: `/health`
3. Provide the required IAM roles:
   - **Task execution role** (for pulling images/logs)
   - **Infrastructure role** (for provisioning networking + load balancer)
4. Add environment variables:
   - `OPENAI_API_KEY` = your OpenAI API key
5. Create the service and copy the generated HTTPS service URL.

### 4) Frontend: Configure API URL

Create `frontend/.env.production`:

```
VITE_API_BASE_URL=https://YOUR-ECS-EXPRESS-URL
```

### 5) Frontend: Build

```bash
cd frontend
npm install
npm run build
```

This creates `frontend/dist`.

### 6) Frontend: S3 Static Hosting

1. Create an S3 bucket (e.g. `ai-math-assistant-frontend`).
2. Disable **Block all public access**.
3. Enable **Static website hosting**.
4. Set **Index document** to `index.html`.
5. Upload the contents of `frontend/dist` to the bucket.

### 7) Frontend: CloudFront

1. Create a CloudFront distribution.
2. Origin: your S3 bucket.
3. Default root object: `index.html`.
4. SPA routing fix (recommended):
   - Add custom error responses:
     - 403 → `/index.html` with 200
     - 404 → `/index.html` with 200

### 8) Verify

- ECS Express Mode: visit `https://YOUR-ECS-EXPRESS-URL/health`
- CloudFront: visit the distribution URL and try a query

### Notes
- CORS is already open (`*`) in the backend.
- Keep API keys only in ECS Express Mode env vars, never in the image or frontend.
