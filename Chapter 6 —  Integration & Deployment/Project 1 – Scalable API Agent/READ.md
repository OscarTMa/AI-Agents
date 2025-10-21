# 🔍 Project 1 – Scalable API Agent
## 🎯 Objective

Deploy a FastAPI agent that processes user queries, stores memory in Redis, and runs in Docker.

## 🧠 Architecture

User → FastAPI → Redis Memory → Response

## 🧰 Stack

FastAPI for REST API

Redis for in-memory data

Docker for containerization

🧩 Implementation
# Build Docker image
````bash
docker build -t api-agent .
````

# Run locally
````bash
docker run -p 8080:8080 api-agent
````

# Access endpoint
````bash
http://localhost:8080/agent
````

☁️ **Deployment**

Deploy using:
- AWS ECS or Google Cloud Run
- Kubernetes for orchestration
- Prometheus + Grafana for monitoring

