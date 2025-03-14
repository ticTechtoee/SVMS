import os
import django

# Ensure the project name matches your actual Django project folder name (case-sensitive)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SVMS.settings")
django.setup()

import numpy as np
import pandas as pd
import joblib
from django.conf import settings
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from vehicleApp.models import VehicleServiceRecord

# Define the model path
MODEL_PATH = os.path.join(settings.BASE_DIR, "predictionApp", "model.pkl")

def load_data():
    """Load data from the VehicleServiceRecord model."""
    records = VehicleServiceRecord.objects.all()

    if not records:
        print("No data available for training.")
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
        return

    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, MODEL_PATH)
    print(f"Model trained and saved at {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
