## AWS Deployment (ECS Fargate + S3/CloudFront)

This guide deploys the FastAPI backend to **Amazon ECS Fargate** (from ECR) and the React frontend to **S3 + CloudFront**.

### Prerequisites
- AWS account and IAM user with access to ECR, ECS, ELB, S3, CloudFront, and IAM
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

### 2) Backend: IAM Role Setup

ECS Fargate requires a **task execution role** so ECS can pull the image and write logs.

#### Task Execution Role

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

### 3) Backend: Create ECS Fargate Service

1. Open **ECS** -> **Clusters** -> choose a cluster (or create one).
2. Create a **task definition**:
   - Launch type: **Fargate**
   - Task execution role: `ecsTaskExecutionRole`
   - Task role: leave empty unless your app needs direct access to AWS services
   - Container image: select `ai-math-assistant:latest` from ECR
   - Container port: `8000`
   - Environment variables:
     - `OPENAI_API_KEY` = your OpenAI API key
3. Create a **service** from that task definition:
   - Launch type: **Fargate**
   - Desired tasks: `1`
   - Networking:
     - Choose your VPC
     - Select subnets for the tasks
     - Assign a security group that allows traffic from the load balancer to port `8000`
   - Load balancing:
     - Use an **Application Load Balancer**
     - Forward traffic to container port `8000`
     - Set the target group health check path to `/health`
4. Create the service and copy the ALB DNS name once the task is healthy.

### 4) Frontend: Configure API URL

Create `frontend/.env.production`:

```bash
VITE_API_BASE_URL=http://YOUR-ALB-DNS-NAME
```

### 5) Frontend: Build

```bash
cd frontend
npm install
npm run build
```

This creates `frontend/dist`.

### 6) Frontend: S3 Static Hosting

1. Create an S3 bucket (for example `ai-math-assistant-frontend`).
2. Disable **Block all public access** if you are using the S3 website endpoint directly.
3. Enable **Static website hosting**.
4. Set **Index document** to `index.html`.
5. Upload the contents of `frontend/dist` to the bucket.

### 7) Frontend: CloudFront

1. Create a CloudFront distribution.
2. Origin: your S3 bucket.
3. Default root object: `index.html`.
4. For SPA routing, add custom error responses:
   - 403 -> `/index.html` with response code `200`
   - 404 -> `/index.html` with response code `200`

### 8) Verify

- ECS Fargate: visit `http://YOUR-ALB-DNS-NAME/health`
- CloudFront: visit the distribution URL and try a query

### Notes

- CORS is already configured in the backend.
- Keep API keys only in ECS task environment variables, never in the image or frontend.
- If your frontend is served over HTTPS, your backend should also be exposed over HTTPS to avoid mixed-content errors.
