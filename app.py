import pickle
import flask
from datetime import datetime
from flask import Flask, request
import time
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

app = Flask(__name__)


#loadin the saved random forest classifier model
model_pickle = open("./driver_attrion_rf.sav", "rb")
clf = pickle.load(model_pickle)


@app.route("/ping", methods=["GET"])
def ping():
    return {"message": "Pinging the model successful!!"}

@app.route("/predict", methods=["POST"])
def prediction():

    driver_params = request.get_json()

    city_dict = pickle.load(open(r'./city_dict.pkl', 'rb'))
    city = city_dict[driver_params['City']]

    gender_dict = {'M':0, 'F':1}
    gender = gender_dict[driver_params['Gender']]
    #date = time.strptime(driver_params['Joining_date'])
    workingdays = driver_params['Working_days']#(datetime.now() - date).days
    total_profits = 0 if driver_params['Business_value']<0 else driver_params['Business_value']

    #age	city	joining_designation	grade	
    #quarterly_rating	grade_change	inc_change	
    # rating_change	income	total_profits	workingdays
    
    input_params = [[driver_params['Age'], city, driver_params['Joining_designation'], \
               driver_params['Grade'], driver_params['Quarterly_rating'], \
               driver_params['Grade_change'], driver_params['Income_change'], \
               driver_params['Rating_change'], driver_params['Income'], \
               total_profits, workingdays]]

    rf_model = pickle.load(open(r'./driver_attrion_rf.sav', 'rb'))

    prediction = rf_model.predict(input_params)
    probs = rf_model.predict_proba(input_params)

    if prediction == 0:
        pred = f'Not Leaving, with Probability {(probs[0,0])*100} %'
    else:
        pred = f'Attrition*, with Probability {probs[0,1]*100} %'

    return {"Driver_Churn_Prediction": pred}

@app.route('/get_params', methods=["GET"])
def get_params_structure():

    parameters = {
                    "Age": '<Applicant Age in numbers>',
                    "Gender":"<M or F>",
                    "City": "<C1 to C29>",        
                    "Joining_designation":"<1 to 5>",
                    "Grade": "<1 to 5>",
                    "Quarterly_rating":"<1 to 5>",
                    "Grade_change":"<-5 to 5>",
                    "Income_change": "<-inf to inf>",
                    "Rating_change":"<-5 to 5>",
                    "Income":"<Numerical Value>",
                    "Business_value":"<-inf to inf>",
                    "Working_days": "<Positive number>"
                    }
    
    return parameters

