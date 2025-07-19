from flask import Blueprint, request, jsonify
import joblib
import os

prediction_bp = Blueprint('prediction', __name__)

# Load mô hình đã huấn luyện
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'heart_attack_model.pkl')
model = joblib.load(model_path)

@prediction_bp.route('/predict', methods=['POST'])
def predict_heart_attack():
    try:
        data = request.get_json()
        
        # Lấy các tính năng từ dữ liệu đầu vào
        features = [
            data.get('age', 0),
            data.get('cholesterol', 0),
            data.get('heart_rate', 0),
            data.get('diabetes', 0),
            data.get('family_history', 0),
            data.get('smoking', 0),
            data.get('obesity', 0),
            data.get('alcohol_consumption', 0),
            data.get('exercise_hours_per_week', 0),
            data.get('diet', 0),
            data.get('previous_heart_problems', 0),
            data.get('medication_use', 0),
            data.get('stress_level', 0),
            data.get('sedentary_hours_per_day', 0),
            data.get('income', 0),
            data.get('bmi', 0),
            data.get('triglycerides', 0),
            data.get('physical_activity_days_per_week', 0),
            data.get('sleep_hours_per_day', 0),
            data.get('blood_sugar', 0),
            data.get('ck_mb', 0),
            data.get('troponin', 0),
            data.get('gender', 0),
            data.get('systolic_blood_pressure', 0),
            data.get('diastolic_blood_pressure', 0)
        ]
        
        # Dự đoán
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]
        
        return jsonify({
            'prediction': int(prediction),
            'probability': {
                'no_risk': float(probability[0]),
                'risk': float(probability[1])
            },
            'message': 'Có nguy cơ đau tim' if prediction == 1 else 'Không có nguy cơ đau tim'
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

