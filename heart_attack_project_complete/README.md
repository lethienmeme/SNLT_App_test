# Dự án Dự đoán Nguy cơ Đau tim

## Mô tả
Ứng dụng web dự đoán nguy cơ đau tim sử dụng React (frontend) và Flask (backend) với chatbot tích hợp.

## Cấu trúc dự án
```
├── heart_attack_api/          # Backend Flask
│   ├── src/
│   │   ├── main.py           # File chính của Flask
│   │   ├── routes/           # API routes
│   │   │   ├── prediction_simple.py  # API dự đoán
│   │   │   └── user.py       # API người dùng
│   │   ├── models/           # Database models
│   │   ├── static/           # Frontend build files
│   │   └── database/         # SQLite database
│   └── requirements.txt      # Python dependencies
│
└── heart-attack-frontend/     # Frontend React
    ├── src/
    │   ├── App.jsx           # Component chính
    │   ├── components/ui/    # UI components
    │   └── assets/           # Static assets
    ├── package.json          # Node.js dependencies
    └── vite.config.js        # Vite configuration
```

## Cài đặt và chạy

### Backend (Flask)
1. Di chuyển vào thư mục backend:
   ```bash
   cd heart_attack_api
   ```

2. Tạo môi trường ảo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # hoặc
   venv\Scripts\activate     # Windows
   ```

3. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Chạy server:
   ```bash
   python src/main.py
   ```

### Frontend (React)
1. Di chuyển vào thư mục frontend:
   ```bash
   cd heart-attack-frontend
   ```

2. Cài đặt dependencies:
   ```bash
   npm install
   # hoặc
   pnpm install
   ```

3. Chạy development server:
   ```bash
   npm run dev
   # hoặc
   pnpm run dev
   ```

4. Build cho production:
   ```bash
   npm run build
   # hoặc
   pnpm run build
   ```

## Tính năng chính

### Form dự đoán nguy cơ đau tim
- Ngày sinh
- Giới tính
- Cholesterol (mg/dL)
- Số giờ tập thể dục/tuần
- Số giờ ngồi/ngày
- Cân nặng (kg) và Chiều cao (cm)
- BMI (tự động tính)
- Triglycerides (mg/dL)
- Số giờ ngủ/ngày
- Đường huyết (mg/dL)
- CK-MB (ng/mL)
- Troponin (ng/mL)
- Huyết áp tâm thu và tâm trương (mmHg)
- Các checkbox: Tiểu đường, Tiền sử gia đình, Hút thuốc, Béo phì

### Chatbot tư vấn
- Trả lời câu hỏi về yếu tố nguy cơ đau tim
- Tư vấn về cách phòng ngừa
- Thông tin về triệu chứng

## API Endpoints

### POST /api/predict
Dự đoán nguy cơ đau tim dựa trên thông tin sức khỏe.

**Request body:**
```json
{
  "age": 45,
  "cholesterol": 200,
  "systolic_blood_pressure": 120,
  "diastolic_blood_pressure": 80,
  "bmi": 25,
  "diabetes": 0,
  "smoking": 0,
  "family_history": 1,
  ...
}
```

**Response:**
```json
{
  "prediction": 0,
  "probability": {
    "no_risk": 0.7,
    "risk": 0.3
  },
  "message": "Không có nguy cơ đau tim"
}
```

### POST /api/chat
Chatbot tư vấn sức khỏe.

**Request body:**
```json
{
  "message": "Các yếu tố nguy cơ đau tim là gì?"
}
```

**Response:**
```json
{
  "response": "Các yếu tố nguy cơ đau tim bao gồm: tuổi tác, cholesterol cao, huyết áp cao..."
}
```

## Triển khai
Ứng dụng đã được triển khai tại: https://g8h3ilcvgq38.manus.space

## Công nghệ sử dụng
- **Frontend:** React, Vite, Tailwind CSS, shadcn/ui
- **Backend:** Flask, Flask-CORS
- **Database:** SQLite
- **Deployment:** Manus Platform

## Lưu ý
- Kết quả dự đoán chỉ mang tính chất tham khảo
- Nên tham khảo ý kiến bác sĩ chuyên khoa
- Không thay thế cho việc khám sức khỏe định kỳ

