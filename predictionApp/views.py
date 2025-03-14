import os
import joblib
import numpy as np
from .forms import PredictionForm
import pandas as pd
from vehicleApp.models import Vehicle
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from vehicleApp.models import VehicleServiceRecord

# Define the model path
MODEL_PATH = os.path.join(settings.BASE_DIR, "predictionApp", "model.pkl")

def load_data():
    """Load data from the VehicleServiceRecord model."""
    records = VehicleServiceRecord.objects.all()

    if not records:
        return None, None

    data = []
    for record in records:
        data.append([record.vehicle.id, record.mileage_at_service, record.maintenance_category.id])

    df = pd.DataFrame(data, columns=["vehicle_id", "mileage", "category"])

    X = df[["vehicle_id", "mileage"]]
    y = df["mileage"].shift(-1).fillna(df["mileage"])  # Predicting next mileage

    return X, y

def train_model():
    """Train the prediction model and save it."""
    X, y = load_data()

    if X is None or y is None:
        return "No data available for training."

    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, MODEL_PATH)
    return "Model trained successfully."

def train_model_view(request):
    """Django view to trigger model training from a web request."""
    message = train_model()
    return HttpResponse(message)









def predict_next_service(vehicle_id, current_mileage):
    try:
        model = joblib.load(MODEL_PATH)
        prediction = model.predict([[vehicle_id, current_mileage]])
        return round(prediction[0])
    except:
        return "Model not trained yet."

def predict_view(request):
    form = PredictionForm()
    vehicles = Vehicle.objects.all()  # Fetch all vehicles

    if request.method == "GET" and "vehicle_id" in request.GET and "mileage" in request.GET:
        vehicle_id = int(request.GET["vehicle_id"])
        current_mileage = int(request.GET["mileage"])
        prediction = predict_next_service(vehicle_id, current_mileage)
        return render(request, "predictionApp/predict.html", {
            "form": form,
            "vehicles": vehicles,
            "next_service_mileage": prediction
        })

    return render(request, "predictionApp/predict.html", {
        "form": form,
        "vehicles": vehicles
    })