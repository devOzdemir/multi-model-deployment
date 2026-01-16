# Multi-Model Deployment API on Kubernetes

This project is a comprehensive **MLOps application** that deploys four different machine learning models using **FastAPI**, **SQLModel**, **Docker**, and **Kubernetes**.  
It provides endpoints for **Iris classification**, **Advertising sales prediction**, **Sentiment analysis using TensorFlow**, and **Product Review analysis via Gemini LLM**.

---

## 1. Project Structure

.
├── main.py
├── models.py
├── database.py
├── routers/
│   ├── iris.py
│   ├── advertising.py
│   ├── tensorflow_model.py
│   └── llm.py
├── saved_models/
│   ├── *.pkl
│   └── *.h5
├── data/
│   └── *.csv
├── k8s-app.yaml         # Kubernetes Deployment & Service for FastAPI
├── k8s-postgres.yaml    # Kubernetes Deployment, Service & PVC for DB
├── docker-compose.yml
├── Dockerfile
└── .env

The project follows a modular structure for scalability and maintainability.

### File Descriptions

- **main.py**: Entry point of the FastAPI application.
- **models.py**: SQLModel database schemas and Pydantic request/response models.
- **database.py**: PostgreSQL connection logic and automatic table creation.
- **k8s-*.yaml**: Kubernetes configuration files for deployment.
- **saved_models/**: Serialized trained models.

---

## 2. Setup and Installation

### Prerequisites

- Docker & Docker Desktop (Kubernetes enabled)
- kubectl CLI
- Google API Key (for Gemini LLM)


### Github

Clone the repo:
`git clone https://github.com/devOzdemir/multi-model-deployment.git`

### Environment Variables

Create a `.env` file in the root directory:
```bash
POSTGRES_USER=train
POSTGRES_PASSWORD=Ankara06
POSTGRES_DB=traindb
GOOGLE_API_KEY=your_gemini_api_key_here
```
---
## 3. Deployment Instructions (Kubernetes)
This is the recommended way to run the application for production-like environments.

Step 1: Create Kubernetes Secrets
Load your environment variables into Kubernetes securely:
`kubectl create secret generic mlops-secrets --from-env-file=.env`

Step 2: Build Docker Image
Build the image locally so Kubernetes can use it:
`docker build -t mlops-app:latest .`

Step 3: Deploy Database
Deploy PostgreSQL with Persistent Volume Claim:
`kubectl apply -f k8s-postgres.yaml`

Step 4: Deploy Application
Deploy the FastAPI application (2 Replicas + LoadBalancer):
`kubectl apply -f k8s-app.yaml`

Step 5: Verify & Access
Check the status of pods and services:
`kubectl get all`

Once the pods are Running, access the application at:

- API URL: http://localhost:80

- Swagger UI: http://localhost:80/docs
---
## 4. Alternative: Running with Docker Compose (Local Dev)
If you want to run quickly without Kubernetes:
`docker compose up -d --build`

- Access via: http://localhost:8000/docs
---
## 5. API Endpoints and Testing
**Iris Species Prediction**
- Endpoint: `POST /iris/prediction/iris`

```
{
  "SepalLengthCm": 5.1,
  "SepalWidthCm": 3.5,
  "PetalLengthCm": 1.4,
  "PetalWidthCm": 0.2
}
```
**Advertising Sales Prediction**
- Endpoint: `POST /advertising/prediction/advertising`

```
{
  "tv": 230.1,
  "radio": 37.8,
  "newspaper": 69.2
}
```

**Sentiment Analysis (TensorFlow)**
- Endpoint: `POST /tensorflow/prediction/comment`
```
{
  "comment": "This movie was an absolute masterpiece of cinematography!"
}
```

**Product Review Analysis (Gemini LLM)**
- Endpoint: POST /product-review/llm/chat
```
{
  "user": "john_doe",
  "product": "Wireless Headphones",
  "review": "Amazing sound quality, but the battery life is a bit short."
}
```
---
## 6. Database Schema
##### The application uses PostgreSQL to persist all prediction results. Tables are created automatically at application startup.

- advertising: Stores TV, Radio, Newspaper inputs and sales predictions.

- iris: Stores sepal/petal measurements and predicted species.

- products_review_rates: Stores Gemini LLM analysis.

- commentpredict: Stores sentiment analysis results.
---
## 7. Tech Stack
- Framework: FastAPI

- Containerization: Docker & Docker Compose

- Orchestration: Kubernetes (Deployments, Services, Secrets, PVC)

- Database: PostgreSQL (SQLModel/SQLAlchemy)

- ML Libraries: TensorFlow, Scikit-learn, LangChain