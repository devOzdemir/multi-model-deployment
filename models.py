"""
Database models using SQLModel for product reviews.
"""

from datetime import datetime
from typing import Optional, Literal
from sqlmodel import SQLModel, Field


class Advertising(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tv: float
    radio: float
    newspaper: float
    prediction: float
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str


class Iris(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    prediction: str
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str


class ProductReviewRate(SQLModel, table=True):
    __tablename__ = "products_review_rates"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_info: str = Field(description="User information or identifier")
    review: str = Field(description="The original review text")
    product: str = Field(description="Product name or identifier")
    rate: Optional[int] = Field(default=None, description="Rating 1-5")
    sentiment: Optional[str] = Field(
        default=None, description="Positive or negative sentiment"
    )
    key_points: Optional[str] = Field(
        default=None, description="Key points as JSON string"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When the review was processed"
    )


# Product Review Analysis
class ProductReview(SQLModel):
    """Analysis of a product review."""

    # Rating with validation constraints
    rating: int | None = Field(
        description="The rating of the product (1-5)",
        ge=1,  # minimum value = 1
        le=5,  # maximum value = 5
    )
    # Sentiment with restricted values
    sentiment: Literal["positive", "negative"] = Field(
        description="The sentiment of the review"
    )
    # List of key points
    key_points: list[str] = Field(
        description="Key points from the review. Lowercase, 1-3 words each."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "rating": 5,
                "sentiment": "positive",
                "key_points": ["great quality", "fast delivery", "easy to use"],
            }
        }


class AnalyzedReview(SQLModel):
    user: str = Field(description="User information or identifier")
    product: str = Field(description="Product name or identifier")
    review: str = Field(description="The original review text")

    class Config:
        json_schema_extra = {
            "example": {
                "user": "john_doe",
                "product": "Wireless Headphones XYZ",
                "review": "Amazing product! 5 stars. Quick delivery and great quality, but quite pricey.",
            }
        }


class RequestIris(SQLModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

    class Config:
        json_schema_extra = {
            "example": {
                "SepalLengthCm": 5.1,
                "SepalWidthCm": 3.5,
                "PetalLengthCm": 1.4,
                "PetalWidthCm": 0.2,
            }
        }


class RequestAdvertising(SQLModel):
    tv: float
    radio: float
    newspaper: float

    class Config:
        json_schema_extra = {
            "example": {
                "tv": 230.1,
                "radio": 37.8,
                "newspaper": 69.2,
            }
        }


class Comment(SQLModel):
    comment: str

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "Among the many lovely details of this film are views about the gender barriers in the Middle East and the customs of a city that, while modern, is still a culture of men. As Juliette and Tareq wander the streets of Cairo we recognize subtleties that exist, subtleties that director Nadda never forces. The gorgeous cinematography is by Luc Montpellier and the musical score is by Niall Byrne. This film is more a poem than a story, a welcome change from the usual youngster-oriented love stories and more of a mature episode of ageless flirtation."
            }
        }


class CommentPredict(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    comment: str
    sentiment: str
    client_ip: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
