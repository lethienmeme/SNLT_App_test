import pickle
import time
import numpy as np
import pandas as pd
import beautifulsoup4 as bs
import matplotlib.pyplot as plt
import requests
import threading
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# This is a main script for an app that receive data from a device like a Fitbit-liked wearable device and load the measured data to file 
# that only alarm the predictions if the data is extreme outlier or prediction indicates a health issue.
""" Inputs: 'Age',
            'Cholesterol',
            'Heart rate',
            'Exercise Hours Per Week',
            'Sedentary Hours Per Day',
            'BMI',
            'Triglycerides',
            'Sleep Hours Per Day',
            'Blood sugar',
            'CK-MB',
            'Troponin   ',
            'Systolic blood pressure',
            'Diastolic blood pressure'
"""
def load_model(file_path:str):
    with open(file_path, 'rb') as f:
        model = pickle.load(f)
    return model


def continuous_predicting(model, df):
    #if the a part of data is missing, stay on and print the previous prediction
    if df is None or df.isna().any().any():
        print("No data available for prediction. Waiting for new data...")
    else:
        predictions = model.predict(df)
    return predictions
    
    ###threading.Timer(10, continuous_predicting, [model, data]).start()  # Update every 10 seconds
        
def alarm_raise(level: int):
    if level == 0:   
        return
    if level == 1:
        return "Alert"
    if level == 2:
        return "Critical Alert"
    
def prediction_conditions(predictions):
    if predictions is None or len(predictions) == 0:
        raise ValueError("No predictions available for evaluation.")
# TODO: Implement the logic to raise an alarm based on raw input(extreme outlier detection or other criteria such as prediction value, changes/changes frequency in prediction, etc.)
# but pass a number of inputs before alarm is raised to avoid false alarms.
    for prediction in predictions:
        if prediction < 0.5:
            alarm = alarm_raise(1)
        elif prediction < 0.2:
            alarm = alarm_raise(2)
        else:
            alarm = alarm_raise(0)  # *** Need retouch

def heart_rate_alarm(data):
    """Age Group	Normal Resting Heart Rate (bpm)
    0-4 years	90-130 bpm
    5-9 years	80-110 bpm
    10-14 years	70-100 bpm
    15-19 years	60-90 bpm
    20-44 years	60-80 bpm
    45-69 years	60-85 bpm
    70-74 years	60-90 bpm
    75-79 years	60-90 bpm
    80-84 years	60-95 bpm
    85-89 years	60-100 bpm
    90-94 years	60-100 bpm
    95-99 years	60-100 bpm"""
    # Example logic to check if heart rate is within normal range
    age = data['Age']
    heart_rate = data['Heart rate']
    if age is None or heart_rate is None:
        raise ValueError("Age and Heart rate must be provided for heart rate prediction.")
    if not isinstance(age, (int, float)) or not isinstance(heart_rate, (int, float)):
        raise TypeError("Age and Heart rate must be numeric values.")
    if age < 0 or heart_rate < 0:
        if age < 5:
            return alarm_raise(0) if 90 <= heart_rate <= 130 else alarm_raise(1)
        elif age < 10:
            return alarm_raise(0) if 80 <= heart_rate <= 110 else alarm_raise(1)
        elif age < 15:
            return alarm_raise(0) if 70 <= heart_rate <= 100 else alarm_raise(1)
        elif age < 20:
            return alarm_raise(0) if 60 <= heart_rate <= 90 else alarm_raise(1)
        elif age < 45:
            return alarm_raise(0) if 60 <= heart_rate <= 80 else alarm_raise(1)
        elif age < 70:
            return alarm_raise(0) if 60 <= heart_rate <= 85 else alarm_raise(1)
        elif age < 80:
            return alarm_raise(0) if 60 <= heart_rate <= 90 else alarm_raise(1)
        elif age < 85:
            return alarm_raise(0) if 60 <= heart_rate <= 95 else alarm_raise(1)
        elif age < 90:
            return alarm_raise(0) if 60 <= heart_rate <= 100 else alarm_raise(1)
        elif age < 95:
            return alarm_raise(0) if 60 <= heart_rate <= 100 else alarm_raise(1)
        else:
            return alarm_raise(0) if 60 <= heart_rate <= 100 else alarm_raise(1)
    

def prediction_shown(predictions):
    pass

def plot_predictions(predictions):
# Store predictions in a DataFrame and plot them, continuously update over time, plot 10 latest predictions.
    df = pd.DataFrame(predictions, columns=['Predictions'])
    df['Timestamp'] = pd.to_datetime('now')
    plt.figure(figsize=(10, 5))
    plt.plot(df['Timestamp'], df['Predictions'], marker='o')
    plt.title('Predictions Over Time')
    plt.xlabel('Time')
    plt.ylabel('Predictions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    ### threading.Timer(10, plot_predictions, [predictions]).start()  # Update every 10 seconds

def userInput(DOB=None, Cholesterol=170,
            Exercise_Hours_Per_Week=3, Sedentary_Hours_Per_Day=5,
            Weight=70, Height=1.75, Triglycerides=150,
            Sleep_Hours_Per_Day=7, Blood_sugar=90,
            CK_MB=5, Troponin=0.01,
            Systolic_blood_pressure=120, Diastolic_blood_pressure=80):
    """'DOB',
    'Cholesterol',
    'Exercise Hours Per Week',
    'Sedentary Hours Per Day',
    Weight and height for 'BMI',
    'Triglycerides',
    'Sleep Hours Per Day',
    'Blood sugar',
    'CK-MB',
    'Troponin',
    'Systolic blood pressure',
    'Diastolic blood pressure'"""
    # Convert DOB to age DOB is datetime class is DOB is None set defult age to 30
    if DOB is None:
        Age = 30  # Default age if DOB is not provided
    else:
        if not isinstance(DOB, (str, int)):
            raise TypeError("DOB must be a string or integer representing a date.")
        try:
            DOB = pd.to_datetime(DOB)
            Age = (pd.Timestamp.now() - DOB).days // 365
        except Exception as e:
            raise ValueError(f"Invalid date format for DOB: {e}")
    
    data = {
        'Age': Age,
        'Cholesterol': Cholesterol,
        'Exercise Hours Per Week': Exercise_Hours_Per_Week,
        'Sedentary Hours Per Day': Sedentary_Hours_Per_Day,
        'BMI' : Weight / (Height ** 2),
        'Triglycerides': Triglycerides,
        'Sleep Hours Per Day': Sleep_Hours_Per_Day,
        'Blood sugar': Blood_sugar,
        'CK-MB': CK_MB,
        'Troponin': Troponin,
        'Systolic blood pressure': Systolic_blood_pressure,
        'Diastolic blood pressure': Diastolic_blood_pressure
    }
def data_building(measured_heart_rate,userInput):
    """Take data from userInput combine with device measured data(Heart rate) and return a DataFrame.
    Each instance of data should be a row in the DataFrame, with the timestamp as an index.
    This build a row dict with data from userInput and device measured data(Heart rate) and return a DataFrame.
    """
    data = userInput
    if measured_heart_rate is not None:
        data['Heart rate'] = measured_heart_rate
    else:
        raise ValueError("Measured heart rate must be provided.")
    df = pd.DataFrame([data])
    df.set_index(pd.to_datetime('now'), inplace=True)  # Set the current time
    return df
def data_processing(df):
    # Normalize the data for model input
    df['Age'] = df['Age'] / 100
    df['Heart rate'] = df['Heart rate'] / 1800 
    df['Cholesterol'] = df['Cholesterol'] / 400
    df['Exercise Hours Per Week'] = df['Exercise Hours Per Week'] / 42
    df['Sedentary Hours Per Day'] = df['Sedentary Hours Per Day'] / 24
    df['BMI'] = df['BMI'] / 40
    df['Triglycerides'] = df['Triglycerides'] / 300
    df['Sleep Hours Per Day'] = df['Sleep Hours Per Day'] / 10
    df['Blood sugar'] = df['Blood sugar'] / 369
    df['CK-MB'] = df['CK-MB'] / 104
    df['Troponin'] = df['Troponin']
    df['Systolic blood pressure'] = df['Systolic blood pressure'] / 220
    df['Diastolic blood pressure'] = df['Diastolic blood pressure'] / 150
    df['Diabetes'] = 0.652554
    df['Family History'] = 0.488749
    df['Smoking'] = 0.902421
    df['Obesity'] = 0.500160
    df['Alcohol Consumption'] = 0.600192
    df['Diet'] = 1.000320
    df['Previous Heart Problems'] = 0.495254
    df['Medication Use'] = 0.499947
    df['Stress Level'] = 5.477338
    df['Income'] = 0.494889
    
    return df
def main():
    if __name__=='__main__':
        