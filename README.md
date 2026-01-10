#  FastAPI Multi-Model Deployment with Docker

## Overview
Deploy a comprehensive FastAPI application with multiple ML endpoints using Docker, PostgreSQL for result storage, and pickle-serialized models (without MLflow).

## Project Structure
Your application should include the following components:
- FastAPI main application with 4 distinct ML endpoints
- PostgreSQL database integration for storing prediction results
- Docker containerization
- Model serialization using pickle/joblib (no MLflow)

## Required Endpoints

### 1. LLM Chat Endpoint (`/product-review`)
- **Purpose**: Product review sentiment analysis using LangChain LLM
- **Input**: Product review text
- **Output**: Sentiment classification and confidence score
- **Model**: LangChain-based LLM integration

### 2. Deep Learning Endpoint (`/tensorflow`)
- **Purpose**: Text sentiment analysis using TensorFlow/Keras
- **Input**: Text for sentiment analysis
- **Output**: Sentiment prediction (positive/negative) with probability
- **Model**: TensorFlow deep learning model
- **Additional**: Include tokenizer as pickle file

### 3. Advertising Revenue Prediction (`/advertising`)
- **Purpose**: Predict advertising revenue based on input features
- **Input**: Advertising campaign features (TV, Radio, Newspaper spend)
- **Output**: Predicted revenue
- **Model**: Scikit-learn regression model (pickle format)

### 4. Iris Classification (`/iris`)
- **Purpose**: Iris flower species classification
- **Input**: Sepal/Petal measurements (length, width)
- **Output**: Iris species prediction with confidence
- **Model**: Scikit-learn classification model (pickle format)

## Technical Requirements

### 1. Database Integration
- **Database**: PostgreSQL
- **Purpose**: Store all prediction results with timestamps
- **Models**: Create appropriate database models for each endpoint's results
- **Connection**: Use SQLModel/SQLAlchemy for ORM
- **Environment**: Database credentials via environment variables

### 2. Model Storage
- **Format**: All models must be saved as pickle files using `joblib`
- **Location**: Store models in `saved_models/` directory
- **Prohibition**: Do NOT use MLflow for model management
- **Files**: Include tokenizer.pkl for deep learning endpoint

### 3. Docker Requirements
- **Dockerfile**: Create optimized multi-stage Dockerfile
- **Base Image**: Use appropriate Python base image
- **Dependencies**: Install from requirements.txt
- **Environment**: Configure environment variables for database
- **Health Checks**: Include health check endpoint

### 4. Application Structure
```
project/
├── main.py                 # FastAPI main application
├── models.py              # Database models (SQLModel/Pydantic)
├── database.py            # Database connection and setup
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── routers/              # API endpoint routers
│   ├── __init__.py
│   ├── product_review_llm.py
│   ├── tensorflow_fastapi.py
│   ├── advertising.py
│   └── iris.py
└── saved_models/         # Pickle model files
    ├── advertising_model.pkl
    ├── iris_model.pkl
    ├── label_encoder.pkl
    ├── tensorflow_model.pkl
    └── tokenizer.pkl
```

## Implementation Steps

### Step 1: Model Training and Serialization
1. Train your models using appropriate datasets
2. Save all models pickle files
3. For TensorFlow model, also save tokenizer as pickle
4. For Iris label encoder as pickel as well

### Step 2: FastAPI Application Development
1. Create main FastAPI application with proper routing
2. Implement database models and connection
3. Create individual routers for each endpoint
4. Add proper error handling and validation
5. Include API documentation with examples

### Step 3: Database Setup
1. Configure PostgreSQL connection
2. Create tables for storing prediction results
3. Implement result logging for each endpoint
4. Test database operations

### Step 4: Dockerization
1. Write optimized Dockerfile
2. Configure environment variables
3. Test local Docker build and run
4. Verify all endpoints work in container

### Step 5: Docker Hub Deployment
1. Tag your image: `<your_dockerhub_username>/vbo-mlops7-fastapi:1.0`
2. Push to Docker Hub
3. Test pulling and running from Docker Hub

## Dependencies (requirements.txt)
```txt
fastapi[all]==0.115.5
uvicorn[standard]==0.32.0
pandas==2.2.3
scikit-learn==1.5.2
joblib==1.4.2
langchain==1.1.0
langchain-google-genai==3.2.0
langchain-community>=0.4.1
psycopg2-binary==2.9.11
tensorflow==2.20.0
sqlmodel==0.0.16
```

## Environment Variables
```env
SQLALCHEMY_DATABASE_URL=postgresql://train:your_password@localhost:5432/traindb
GOOGLE_API_KEY=your_google_api_key
```

## Testing Your Application
1. Start PostgreSQL database locally or via Docker
2. Run your application: `uvicorn main:app --host 0.0.0.0 --port 8000`
3. Visit `http://localhost:8000/docs` for API documentation
4. Test all 4 endpoints with sample data
5. Verify database records are created for each prediction

## Submission Requirements

### 1. Docker Hub Image
- Push your final image to Docker Hub
- Image name: `<your_dockerhub_username>/vbo-mlops7-fastapi:1.0`
- Ensure image is publicly accessible

### 2. Project Submission
- Zip your complete project directory
- Include all source code and model files
- Provide clear README with setup instructions
- Include sample requests for testing each endpoint
- Document environment variable requirements
- Upload zip file to Google Classroom

### 3. Documentation
- API endpoints with example requests/responses
- Model information and performance metrics
- Database schema description
- Docker run instructions with environment variables

## Evaluation Criteria

### Functionality (40 points)
- All 4 endpoints working correctly
- Database integration storing results
- Models loaded from pickle files
- Proper error handling

### Docker Implementation (25 points)
- Optimized Dockerfile
- Successful Docker Hub push
- Container runs without issues
- Proper environment variable configuration

### Code Quality (20 points)
- Clean, well-organized code structure
- Proper separation of concerns (routers, models, database)
- Following FastAPI best practices
- Comprehensive error handling

### Documentation (15 points)
- Clear README with setup instructions
- API documentation via FastAPI docs
- Example requests for testing
- Proper code comments

## Delivery
1. **Docker Hub**: `<your_dockerhub_username>/vbo-mlops7-fastapi:1.0`
2. **Google Classroom**: Zip file with complete project source code
3. **Documentation**: README with setup and testing instructions