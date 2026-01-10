# main.py
import joblib
from fastapi import FastAPI
from routers import product_review_llm, iris, advertising, tensorflow_fastapi
from database import create_db_and_tables

# CRITICAL: Import all table models here so SQLModel metadata detects them
from models import Advertising, Iris, ProductReviewRate, CommentPredict
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="MLOps Multi-Model Deployment API")


# Use the startup event to ensure DB tables are created
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Router inclusions
app.include_router(product_review_llm.router, prefix="/product-review", tags=["LLM"])
app.include_router(iris.router, prefix="/iris", tags=["Iris"])
app.include_router(advertising.router, prefix="/advertising", tags=["Advertising"])
app.include_router(tensorflow_fastapi.router, prefix="/tensorflow", tags=["TensorFlow"])


@app.get("/")
def health_check():
    return {"status": "online"}
