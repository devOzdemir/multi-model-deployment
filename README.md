# Multi-Model Deployment API

This project is a comprehensive **MLOps application** that deploys four different machine learning models using **FastAPI**, **SQLModel**, and **Docker**.  
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
├── docker-compose.yml
├── Dockerfile
└── .env

The project follows a modular structure for scalability and maintainability.
### File Descriptions

- **main.py**  
  Entry point of the FastAPI application.

- **models.py**  
  SQLModel database schemas and Pydantic request/response models.

- **database.py**  
  PostgreSQL connection logic and automatic table creation.

- **routers/**  
  Separate API routers for each machine learning model.

- **saved_models/**  
  Serialized trained models.

- **data/**  
  Datasets used during training and testing.

---

## 2. Setup and Installation

### Prerequisites

- Docker  
- Docker Compose  
- Google API Key (for Gemini LLM)

---

### Environment Variables

Change the `.env.example` file into `.env` in the root directory:
```
POSTGRES_USER=train
POSTGRES_PASSWORD=Ankara06
POSTGRES_DB=traindb
GOOGLE_API_KEY=your_gemini_api_key_here
```
---

### Running with Docker

Build and start all services:

`docker compose up -d --build`

After startup:

- API URL: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs  

---

## 3. API Endpoints and Testing

### Iris Species Prediction

**Endpoint**
`POST /iris/prediction/iris`

**Request Body**
```
{
“SepalLengthCm”: 5.1,
“SepalWidthCm”: 3.5,
“PetalLengthCm”: 1.4,
“PetalWidthCm”: 0.2
}
```
---

### Advertising Sales Prediction

**Endpoint**
`POST /advertising/prediction/advertising`

**Request Body**
```
{
“tv”: 230.1,
“radio”: 37.8,
“newspaper”: 69.2
}
```
---

### Sentiment Analysis (TensorFlow)

**Endpoint**
`POST /tensorflow/prediction/comment`

**Request Body**
```
{
“comment”: “This movie was an absolute masterpiece of cinematography!”
}
```
---

### Product Review Analysis (Gemini LLM)

**Endpoint**
`POST /product-review/llm/chat`

**Request Body**
```
{
“user”: “john_doe”,
“product”: “Wireless Headphones”,
“review”: “Amazing sound quality, but the battery life is a bit short.”
}
```
---

## 4. Database Schema

The application uses **PostgreSQL** to persist all prediction results.  
Tables are created automatically at application startup.

### Tables

- **advertising**  
  Stores TV, Radio, Newspaper inputs and sales predictions.

- **iris**  
  Stores sepal/petal measurements and predicted species.

- **products_review_rates**  
  Stores Gemini LLM analysis including sentiment, rating (1–5), and key points (JSON).

- **commentpredict**  
  Stores sentiment analysis results for general comments.

---

## 5. Deployment Information

- **Docker Hub Image**  
  `devozdemir/vbo-mlops7-fastapi:1.0`

- **Python Version**  
  `3.10-slim`