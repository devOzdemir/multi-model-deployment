import os
import pickle
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from tensorflow.keras.models import load_model
from database import get_db
from models import Comment, CommentPredict

router = APIRouter()

MODEL_PATH = "saved_models/tensorflow_model.h5"
TOKENIZER_PATH = "saved_models/tokenizer.pkl"

_model = None
_tokenizer = None


def get_resources():
    global _model, _tokenizer
    if _model is None:
        if os.path.exists(MODEL_PATH):
            try:
                # compile=False prevents the quantization_config error
                _model = load_model(MODEL_PATH, compile=False)
                print("TensorFlow model loaded successfully (compile=False).")
            except Exception as e:
                print(f"TF Load Failure: {e}")
    if _tokenizer is None:
        if os.path.exists(TOKENIZER_PATH):
            with open(TOKENIZER_PATH, "rb") as f:
                _tokenizer = pickle.load(f)
    return _model, _tokenizer


@router.post("/prediction/comment")
async def predict_sentiment(
    request: Comment, fastapi_req: Request, db: Session = Depends(get_db)
):
    model, tokenizer = get_resources()
    if model is None:
        raise HTTPException(status_code=503, detail="Model resources not ready.")

    try:
        from tensorflow.keras.preprocessing.sequence import pad_sequences

        sequences = tokenizer.texts_to_sequences([request.comment])
        tokenized = pad_sequences(sequences, padding="post", maxlen=100)

        # Inference
        prediction = model.predict(tokenized)
        # Check first element of the first prediction result
        label = "positive" if float(prediction[0][0]) > 0.5 else "negative"

        # Database Commit
        new_record = CommentPredict(
            comment=request.comment,
            sentiment=label,
            client_ip=fastapi_req.client.host,
            created_at=datetime.utcnow(),
        )
        db.add(new_record)
        db.commit()  # Save to DB
        db.refresh(new_record)

        return {"sentiment": label}
    except Exception as e:
        print(f"TF ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
