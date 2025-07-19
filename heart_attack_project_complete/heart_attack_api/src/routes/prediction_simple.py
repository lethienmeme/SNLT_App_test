from flask import Blueprint, request, jsonify
import json
import os

prediction_bp = Blueprint('prediction', __name__)

# Hàm dự đoán đơn giản dựa trên quy tắc
def simple_heart_attack_prediction(features):
    """
    Dự đoán nguy cơ đau tim dựa trên các quy tắc đơn giản
    """
    risk_score = 0
    
    # Tuổi (giả sử đã được chuẩn hóa 0-1)
    age = features.get('age', 0)
    if age > 0.6:  # Tuổi cao
        risk_score += 2
    elif age > 0.4:
        risk_score += 1
    
    # Cholesterol
    cholesterol = features.get('cholesterol', 0)
    if cholesterol > 0.7:
        risk_score += 2
    elif cholesterol > 0.5:
        risk_score += 1
    
    # Huyết áp tâm thu
    systolic_bp = features.get('systolic_blood_pressure', 0)
    if systolic_bp > 0.7:
        risk_score += 2
    elif systolic_bp > 0.5:
        risk_score += 1
    
    # BMI
    bmi = features.get('bmi', 0)
    if bmi > 0.7:
        risk_score += 1
    
    # Các yếu tố nguy cơ khác
    if features.get('diabetes', 0) == 1:
        risk_score += 2
    if features.get('smoking', 0) == 1:
        risk_score += 2
    if features.get('family_history', 0) == 1:
        risk_score += 1
    if features.get('previous_heart_problems', 0) == 1:
        risk_score += 3
    
    # Tính xác suất dựa trên điểm số
    if risk_score >= 6:
        probability_risk = 0.8
    elif risk_score >= 4:
        probability_risk = 0.6
    elif risk_score >= 2:
        probability_risk = 0.4
    else:
        probability_risk = 0.2
    
    prediction = 1 if probability_risk > 0.5 else 0
    
    return {
        'prediction': prediction,
        'probability': {
            'no_risk': 1 - probability_risk,
            'risk': probability_risk
        }
    }

@prediction_bp.route('/predict', methods=['POST'])
def predict_heart_attack():
    try:
        data = request.get_json()
        
        # Chuẩn hóa dữ liệu đầu vào (giả sử các giá trị đã được chuẩn hóa từ 0-1)
        features = {
            'age': float(data.get('age', 0)) / 100.0,  # Giả sử tuổi tối đa 100
            'cholesterol': float(data.get('cholesterol', 0)),
            'heart_rate': float(data.get('heart_rate', 0)) / 200.0,  # Giả sử nhịp tim tối đa 200
            'diabetes': int(data.get('diabetes', 0)),
            'family_history': int(data.get('family_history', 0)),
            'smoking': int(data.get('smoking', 0)),
            'obesity': int(data.get('obesity', 0)),
            'alcohol_consumption': int(data.get('alcohol_consumption', 0)),
            'exercise_hours_per_week': float(data.get('exercise_hours_per_week', 0)) / 20.0,
            'diet': int(data.get('diet', 0)),
            'previous_heart_problems': int(data.get('previous_heart_problems', 0)),
            'medication_use': int(data.get('medication_use', 0)),
            'stress_level': float(data.get('stress_level', 0)),
            'sedentary_hours_per_day': float(data.get('sedentary_hours_per_day', 0)) / 24.0,
            'income': float(data.get('income', 0)),
            'bmi': float(data.get('bmi', 0)) / 50.0,  # Giả sử BMI tối đa 50
            'triglycerides': float(data.get('triglycerides', 0)),
            'physical_activity_days_per_week': float(data.get('physical_activity_days_per_week', 0)) / 7.0,
            'sleep_hours_per_day': float(data.get('sleep_hours_per_day', 0)) / 12.0,
            'blood_sugar': float(data.get('blood_sugar', 0)),
            'ck_mb': float(data.get('ck_mb', 0)),
            'troponin': float(data.get('troponin', 0)),
            'gender': int(data.get('gender', 0)),
            'systolic_blood_pressure': float(data.get('systolic_blood_pressure', 0)),
            'diastolic_blood_pressure': float(data.get('diastolic_blood_pressure', 0))
        }
        
        # Dự đoán
        result = simple_heart_attack_prediction(features)
        
        return jsonify({
            'prediction': result['prediction'],
            'probability': result['probability'],
            'message': 'Có nguy cơ đau tim' if result['prediction'] == 1 else 'Không có nguy cơ đau tim'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@prediction_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '').lower()
        
        # Chatbot đơn giản
        if 'xin chào' in message or 'hello' in message:
            response = 'Xin chào! Tôi là chatbot hỗ trợ dự đoán nguy cơ đau tim. Bạn có thể hỏi tôi về các yếu tố nguy cơ đau tim.'
        elif 'nguy cơ' in message or 'yếu tố' in message:
            response = 'Các yếu tố nguy cơ đau tim bao gồm: tuổi tác, cholesterol cao, huyết áp cao, tiểu đường, hút thuốc, béo phì, ít vận động, stress, và tiền sử gia đình.'
        elif 'phòng ngừa' in message or 'ngăn ngừa' in message:
            response = 'Để phòng ngừa đau tim: tập thể dục thường xuyên, ăn uống lành mạnh, không hút thuốc, kiểm soát cân nặng, quản lý stress, và khám sức khỏe định kỳ.'
        elif 'triệu chứng' in message:
            response = 'Triệu chứng đau tim: đau ngực, khó thở, đau lan ra cánh tay/vai/cổ, buồn nôn, chóng mặt, đổ mồ hôi lạnh. Nếu có triệu chứng, hãy gọi cấp cứu ngay!'
        else:
            response = 'Tôi có thể giúp bạn hiểu về nguy cơ đau tim, các yếu tố nguy cơ, cách phòng ngừa và triệu chứng. Bạn muốn biết về điều gì?'
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

