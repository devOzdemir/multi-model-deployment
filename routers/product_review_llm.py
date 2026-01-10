import json
import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from langchain_google_genai import ChatGoogleGenerativeAI
from database import get_db
from models import ProductReview, AnalyzedReview, ProductReviewRate

router = APIRouter()

# Fixed model name to 'gemini-1.5-flash' which is the standard identifier
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0
).with_structured_output(ProductReview)


@router.post("/llm/chat")
async def chat(request: AnalyzedReview, db: Session = Depends(get_db)):
    try:
        analysis = llm.invoke(request.review)

        new_review = ProductReviewRate(
            user_info=request.user,
            review=request.review,
            product=request.product,
            rate=analysis.rating,
            sentiment=analysis.sentiment,
            key_points=json.dumps(analysis.key_points),
            created_at=datetime.utcnow(),
        )

        db.add(new_review)
        db.commit()  # Save to DB
        db.refresh(new_review)

        return {"status": "success", "analysis": analysis}
    except Exception as e:
        print(f"LLM ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")
