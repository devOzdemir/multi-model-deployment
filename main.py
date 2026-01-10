import joblib
from fastapi import FastAPI
from routers import product_review_llm, iris, advertising, tensorflow_fastapi
from database import create_db_and_tables
from dotenv import load_dotenv

# Load env variables at the very beginning
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="ML and LLM Application with Local Models")


# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Include Routers
app.include_router(
    product_review_llm.router, prefix="/product-review", tags=["Product Review LLM"]
)
app.include_router(iris.router, prefix="/iris", tags=["Iris Prediction"])
app.include_router(
    advertising.router, prefix="/advertising", tags=["Advertising Prediction"]
)
app.include_router(
    tensorflow_fastapi.router,
    prefix="/tensorflow",
    tags=["TensorFlow Sentiment Analysis"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the Local ML and LLM Application (MLflow removed)"}
