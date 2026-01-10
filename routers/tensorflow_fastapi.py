from fastapi.routing import APIRouter
from fastapi import Depends, Request
from sqlmodel import Session
from models import Comment, CommentPredict
from database import get_db
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import pickle
from datetime import datetime

router = APIRouter()

# Load model and tokenizer from local saved_models directory
model = joblib.load("saved_models/tensorflow_model.pkl")
with open("saved_models/tokenizer.pkl", "rb") as f:
    tokenizer_loaded = pickle.load(f)


def make_prediction(model, request_dict):
    """Preprocesses text and makes sentiment prediction."""
    comment = [request_dict["comment"]]
    token = tokenizer_loaded.texts_to_sequences(comment)
    token = pad_sequences(token, padding="post", maxlen=100)

    prediction = model.predict(token)
    return "positive" if prediction[0] > 0.5 else "negative"


@router.post("/prediction/comment")
async def predict_sentiment(
    request: Comment, fastapi_req: Request, db: Session = Depends(get_db)
):
    prediction = make_prediction(model, request.model_dump())

    new_prediction = CommentPredict(
        comment=request.comment,
        sentiment=prediction,
        client_ip=fastapi_req.client.host,
        created_at=datetime.utcnow(),
    )

    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)

    return {"sentiment": prediction}
