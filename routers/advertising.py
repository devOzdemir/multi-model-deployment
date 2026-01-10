from fastapi.routing import APIRouter
from fastapi import Depends, Request
from sqlmodel import Session
from models import Advertising, RequestAdvertising
from database import get_db
import joblib
import os

router = APIRouter()

# Load model from local saved_models directory
MODEL_PATH = "saved_models/advertising_model.pkl"
advertising_estimator_loaded = joblib.load(MODEL_PATH)


def make_advertising_prediction(estimator, input_data):
    """Makes prediction using the loaded Scikit-learn regressor."""
    data = [[input_data["tv"], input_data["radio"], input_data["newspaper"]]]
    prediction = estimator.predict(data)
    return float(prediction[0])


def insert_advertising(request, prediction, client_ip, db):
    """Logs the prediction results to PostgreSQL."""
    new_advertising = Advertising(
        tv=request["tv"],
        radio=request["radio"],
        newspaper=request["newspaper"],
        prediction=prediction,
        client_ip=client_ip,
    )
    db.add(new_advertising)
    db.commit()
    db.refresh(new_advertising)
    return new_advertising


@router.post("/prediction/advertising")
def predict_advertising(
    request: RequestAdvertising, fastapi_req: Request, db: Session = Depends(get_db)
):
    prediction = make_advertising_prediction(
        advertising_estimator_loaded, request.model_dump()
    )
    insert_advertising(request.model_dump(), prediction, fastapi_req.client.host, db)
    return {"prediction": prediction}
