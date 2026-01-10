import json
from datetime import datetime
from fastapi.routing import APIRouter
from fastapi import Depends
from sqlmodel import Session
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from models import ProductReview, AnalyzedReview, ProductReviewRate
from database import get_db

router = APIRouter()

# Initialize LangChain Gemini model (Uses API Key from .env)
model = init_chat_model(
    model="gemini-2.0-flash-lite", model_provider="google_genai", max_tokens=500
)

agent = create_agent(
    model=model,
    tools=[],
    response_format=ToolStrategy(schema=ProductReview),
    system_prompt="Analyze product reviews and extract structured data (sentiment, rating, key points).",
)


@router.post("/llm/chat")
def chat(request: AnalyzedReview, db: Session = Depends(get_db)):
    """Analyzes product review using LLM and saves to DB."""
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": f"Analyze this review: '{request.review}'"}
            ]
        }
    )

    structured_data = result["structured_response"]

    review_record = ProductReviewRate(
        user_info=request.user,
        review=request.review,
        product=request.product,
        rate=structured_data.rating,
        sentiment=structured_data.sentiment,
        key_points=json.dumps(structured_data.key_points),
        created_at=datetime.utcnow(),
    )

    db.add(review_record)
    db.commit()
    db.refresh(review_record)

    return structured_data
