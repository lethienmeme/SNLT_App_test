from flask import Flask, request, jsonify
from testing import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/predict', methods=['POST'])

def predict():
    try:
        input_data = request.get_json()
        data = userInput(**input_data)
        model = load_model('model.pkl')  # Load your pre-trained model
        df = data.to_dataframe()  # Convert user input to DataFrame
        data = data_building(df)
        processed_data = data_processing(df)
        data['Heart rate'] = heart_rate_measurement()  # Simulate heart rate measurement
        predictions = continuous_predicting(model, processed_data)
        heart_alarm_level = heart_rate_alarm(data)
        prediction_alarm_level = prediction_conditions(predictions)
        if heart_alarm_level >= prediction_alarm_level:
            alarm_raise(heart_alarm_level)
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route('/')
def index():
    return "Welcome to the Heart Attack Prediction API!"