import os
import json
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from database import engine
from sqlmodel import Session
from models import ProductReviewRate, ProductReview

# Load credentials
load_dotenv()

# Initialize the Gemini model
model = init_chat_model(
    model="gemini-2.0-flash-lite", model_provider="google_genai", max_tokens=500
)

# Create structured output agent
agent = create_agent(
    model=model,
    tools=[],
    response_format=ToolStrategy(schema=ProductReview),
    system_prompt="Analyze product reviews and extract sentiment, rating (1-5), and key points.",
)


def run_test_analysis():
    sample_reviews = [
        {
            "user": "john_doe",
            "product": "Wireless Headphones XYZ",
            "review": "Amazing product! 5 stars. Quick delivery and great quality, but quite pricey.",
        }
    ]

    with Session(engine) as session:
        for sample in sample_reviews:
            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Analyze this: '{sample['review']}'",
                        }
                    ]
                }
            )

            structured = result["structured_response"]

            # Save to DB
            record = ProductReviewRate(
                user_info=sample["user"],
                review=sample["review"],
                product=sample["product"],
                rate=structured.rating,
                sentiment=structured.sentiment,
                key_points=json.dumps(structured.key_points),
                created_at=datetime.utcnow(),
            )
            session.add(record)
            session.commit()
            print(f"Analysis saved for {sample['user']}")


if __name__ == "__main__":
    run_test_analysis()
