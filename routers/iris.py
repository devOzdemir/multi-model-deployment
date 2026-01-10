from fastapi.routing import APIRouter
from models import RequestIris, Iris
from fastapi import Depends, Request
from sqlmodel import Session
from database import get_db
import joblib
import os

router = APIRouter()

# Load model and encoder from local saved_models directory
iris_classifier_loaded = joblib.load("saved_models/iris_model.pkl")
iris_encoder_loaded = joblib.load("saved_models/label_encoder.pkl")


def make_iris_prediction(estimator, encoder, input_data):
    """Predicts iris species and decodes the label."""
    data = [
        [
            input_data["SepalLengthCm"],
            input_data["SepalWidthCm"],
            input_data["PetalLengthCm"],
            input_data["PetalWidthCm"],
        ]
    ]
    prediction_raw = estimator.predict(data)
    prediction_real = encoder.inverse_transform(prediction_raw)
    return prediction_real[0]


def insert_iris(request, prediction, client_ip, db):
    """Logs the iris classification result to the database."""
    new_iris = Iris(
        sepal_length=request["SepalLengthCm"],
        sepal_width=request["SepalWidthCm"],
        petal_length=request["PetalLengthCm"],
        petal_width=request["PetalWidthCm"],
        prediction=prediction,
        client_ip=client_ip,
    )
    db.add(new_iris)
    db.commit()
    db.refresh(new_iris)
    return new_iris


@router.post("/prediction/iris")
def predict_iris(
    request: RequestIris, fastapi_req: Request, db: Session = Depends(get_db)
):
    prediction = make_iris_prediction(
        iris_classifier_loaded, iris_encoder_loaded, request.model_dump()
    )
    insert_iris(request.model_dump(), prediction, fastapi_req.client.host, db)
    return {"prediction": prediction}
