import pytest 
from app import app
import json

@pytest.fixture
def client():
    return app.test_client()

def test_ping(client):
    resp = client.get("/ping")
    assert resp.status_code == 200, "Bad Response"

def test_prediction_1(client):

    test_data =  {
                    "Age": 35,
                    "Gender":"M",
                    "City": "C3",        
                    "Joining_designation":2,
                    "Grade": 2,
                    "Quarterly_rating":1,
                    "Grade_change":0.000000e+00,
                    "Income_change": 0.000000e+00,
                    "Rating_change":0.000000e+00,
                    "Income":70733,
                    "Business_value":-1,
                    "Working_days":  65
                    }

    resp = client.post("/predict", json=test_data)
    assert resp.status_code == 200
    assert resp.json == {"Driver_Churn_Prediction": "Attrition*, with Probability 100.0 %"}

def test_prediction_2(client):

    test_data =  {
                    "Age": 41,
                    "Gender":"M",
                    "City": "C3",        
                    "Joining_designation":1,
                    "Grade": 3,
                    "Quarterly_rating":3,
                    "Grade_change":0.000000e+00,
                    "Income_change": 0.000000e+00,
                    "Rating_change":0.000000e+00,
                    "Income":8.919200e+04,
                    "Business_value":1.346822e+07,
                    "Working_days": 2.221000e+03
                    }

    resp = client.post("/predict", json=test_data)
    assert resp.status_code == 200
    assert resp.json == {"Driver_Churn_Prediction": "Not Leaving, with Probability 81.0 %"}