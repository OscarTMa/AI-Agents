# 🤝 Project 2 – Multi-Agent Deployment
## 🎯 Objective

Deploy multiple collaborating agents using LangChain, Redis, and Pinecone on Kubernetes.

## 🧠 Roles
Agent	Function
Researcher	Gathers contextual data
Summarizer	Produces concise outputs
Evaluator	Validates and refines responses

## ⚙️ Pipeline
- Define agents with LangChain or CrewAI
- Store results in Redis + Pinecone
- Deploy microservices with Kubernetes

## 🧰 Tools
- LangChain / CrewAI
- FastAPI microservices
- Redis + Pinecone
- Docker + Kubernetes

🧱 Deployment Commands
````bash
docker build -t multi-agent-system .
kubectl apply -f k8s/deployment.yaml
kubectl get pods
````
🌐 Endpoint
````bash
http://<your-kubernetes-endpoint>/api/v1/query
````
