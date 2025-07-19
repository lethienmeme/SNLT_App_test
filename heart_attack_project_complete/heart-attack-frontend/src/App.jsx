import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Heart, MessageCircle, Activity, AlertTriangle } from 'lucide-react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    dob: '',
    cholesterol: '',
    exercise_hours_per_week: '',
    sedentary_hours_per_day: '',
    weight: '',
    height: '',
    triglycerides: '',
    sleep_hours_per_day: '',
    blood_sugar: '',
    ck_mb: '',
    troponin: '',
    systolic_blood_pressure: '',
    diastolic_blood_pressure: '',
    gender: 0,
    diabetes: 0,
    family_history: 0,
    smoking: 0,
    obesity: 0
  })

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [chatMessages, setChatMessages] = useState([])
  const [chatInput, setChatInput] = useState('')
  const [showChat, setShowChat] = useState(false)

  const calculateAge = (dob) => {
    if (!dob) return 0
    const today = new Date()
    const birthDate = new Date(dob)
    let age = today.getFullYear() - birthDate.getFullYear()
    const monthDiff = today.getMonth() - birthDate.getMonth()
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--
    }
    return age
  }

  const calculateBMI = (weight, height) => {
    if (!weight || !height) return 0
    const heightInMeters = parseFloat(height) / 100
    return (parseFloat(weight) / (heightInMeters * heightInMeters)).toFixed(2)
  }

  const handleInputChange = (e) => {
    const { name, value, type } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target.checked ? 1 : 0) : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const age = calculateAge(formData.dob)
      const bmi = calculateBMI(formData.weight, formData.height)
      
      const submitData = {
        age: age,
        cholesterol: parseFloat(formData.cholesterol) || 0,
        heart_rate: 70, // Giá trị mặc định
        diabetes: formData.diabetes,
        family_history: formData.family_history,
        smoking: formData.smoking,
        obesity: formData.obesity,
        alcohol_consumption: 0,
        exercise_hours_per_week: parseFloat(formData.exercise_hours_per_week) || 0,
        diet: 0,
        previous_heart_problems: 0,
        medication_use: 0,
        stress_level: 0,
        sedentary_hours_per_day: parseFloat(formData.sedentary_hours_per_day) || 0,
        income: 0,
        bmi: parseFloat(bmi) || 0,
        triglycerides: parseFloat(formData.triglycerides) || 0,
        physical_activity_days_per_week: 0,
        sleep_hours_per_day: parseFloat(formData.sleep_hours_per_day) || 0,
        blood_sugar: parseFloat(formData.blood_sugar) || 0,
        ck_mb: parseFloat(formData.ck_mb) || 0,
        troponin: parseFloat(formData.troponin) || 0,
        gender: formData.gender,
        systolic_blood_pressure: parseFloat(formData.systolic_blood_pressure) || 0,
        diastolic_blood_pressure: parseFloat(formData.diastolic_blood_pressure) || 0
      }

      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submitData)
      })
      
      const result = await response.json()
      setPrediction(result)
    } catch (error) {
      console.error('Lỗi:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleChatSubmit = async (e) => {
    e.preventDefault()
    if (!chatInput.trim()) return

    const userMessage = { type: 'user', message: chatInput }
    setChatMessages(prev => [...prev, userMessage])

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: chatInput })
      })
      
      const result = await response.json()
      const botMessage = { type: 'bot', message: result.response }
      setChatMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Lỗi chat:', error)
    }

    setChatInput('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        <header className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Heart className="h-8 w-8 text-red-500" />
            <h1 className="text-4xl font-bold text-gray-800">Dự đoán nguy cơ đau tim</h1>
          </div>
          <p className="text-gray-600">Nhập thông tin sức khỏe để đánh giá nguy cơ đau tim của bạn</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Form nhập liệu */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  Thông tin sức khỏe
                </CardTitle>
                <CardDescription>
                  Vui lòng nhập đầy đủ thông tin để có kết quả chính xác nhất
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Ngày sinh</label>
                      <Input
                        type="date"
                        name="dob"
                        value={formData.dob}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Giới tính</label>
                      <select
                        name="gender"
                        value={formData.gender}
                        onChange={handleInputChange}
                        className="w-full p-2 border rounded-md"
                        required
                      >
                        <option value={0}>Nam</option>
                        <option value={1}>Nữ</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Cholesterol (mg/dL)</label>
                      <Input
                        type="number"
                        step="0.01"
                        name="cholesterol"
                        value={formData.cholesterol}
                        onChange={handleInputChange}
                        placeholder="Mức cholesterol"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Số giờ tập thể dục/tuần</label>
                      <Input
                        type="number"
                        step="0.1"
                        name="exercise_hours_per_week"
                        value={formData.exercise_hours_per_week}
                        onChange={handleInputChange}
                        placeholder="Giờ tập thể dục"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Số giờ ngồi/ngày</label>
                      <Input
                        type="number"
                        step="0.1"
                        name="sedentary_hours_per_day"
                        value={formData.sedentary_hours_per_day}
                        onChange={handleInputChange}
                        placeholder="Giờ ngồi mỗi ngày"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Cân nặng (kg)</label>
                      <Input
                        type="number"
                        step="0.1"
                        name="weight"
                        value={formData.weight}
                        onChange={handleInputChange}
                        placeholder="Cân nặng"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Chiều cao (cm)</label>
                      <Input
                        type="number"
                        step="0.1"
                        name="height"
                        value={formData.height}
                        onChange={handleInputChange}
                        placeholder="Chiều cao"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">BMI (tự động tính)</label>
                      <Input
                        type="text"
                        value={calculateBMI(formData.weight, formData.height)}
                        placeholder="BMI sẽ được tính tự động"
                        disabled
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Triglycerides (mg/dL)</label>
                      <Input
                        type="number"
                        step="0.01"
                        name="triglycerides"
                        value={formData.triglycerides}
                        onChange={handleInputChange}
                        placeholder="Mức triglycerides"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Số giờ ngủ/ngày</label>
                      <Input
                        type="number"
                        step="0.1"
                        name="sleep_hours_per_day"
                        value={formData.sleep_hours_per_day}
                        onChange={handleInputChange}
                        placeholder="Giờ ngủ mỗi ngày"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Đường huyết (mg/dL)</label>
                      <Input
                        type="number"
                        step="0.01"
                        name="blood_sugar"
                        value={formData.blood_sugar}
                        onChange={handleInputChange}
                        placeholder="Mức đường huyết"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">CK-MB (ng/mL)</label>
                      <Input
                        type="number"
                        step="0.01"
                        name="ck_mb"
                        value={formData.ck_mb}
                        onChange={handleInputChange}
                        placeholder="Mức CK-MB"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Troponin (ng/mL)</label>
                      <Input
                        type="number"
                        step="0.01"
                        name="troponin"
                        value={formData.troponin}
                        onChange={handleInputChange}
                        placeholder="Mức troponin"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Huyết áp tâm thu (mmHg)</label>
                      <Input
                        type="number"
                        step="0.01"
                        name="systolic_blood_pressure"
                        value={formData.systolic_blood_pressure}
                        onChange={handleInputChange}
                        placeholder="Huyết áp tâm thu"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Huyết áp tâm trương (mmHg)</label>
                      <Input
                        type="number"
                        step="0.01"
                        name="diastolic_blood_pressure"
                        value={formData.diastolic_blood_pressure}
                        onChange={handleInputChange}
                        placeholder="Huyết áp tâm trương"
                        required
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        name="diabetes"
                        checked={formData.diabetes === 1}
                        onChange={handleInputChange}
                        className="rounded"
                      />
                      <span className="text-sm">Tiểu đường</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        name="family_history"
                        checked={formData.family_history === 1}
                        onChange={handleInputChange}
                        className="rounded"
                      />
                      <span className="text-sm">Tiền sử gia đình</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        name="smoking"
                        checked={formData.smoking === 1}
                        onChange={handleInputChange}
                        className="rounded"
                      />
                      <span className="text-sm">Hút thuốc</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        name="obesity"
                        checked={formData.obesity === 1}
                        onChange={handleInputChange}
                        className="rounded"
                      />
                      <span className="text-sm">Béo phì</span>
                    </label>
                  </div>

                  <Button type="submit" className="w-full" disabled={loading}>
                    {loading ? 'Đang xử lý...' : 'Dự đoán nguy cơ đau tim'}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Kết quả và Chat */}
          <div className="space-y-6">
            {/* Kết quả dự đoán */}
            {prediction && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5" />
                    Kết quả dự đoán
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center space-y-4">
                    <Badge 
                      variant={prediction.prediction === 1 ? "destructive" : "secondary"}
                      className="text-lg p-2"
                    >
                      {prediction.message}
                    </Badge>
                    <div className="space-y-2">
                      <p className="text-sm text-gray-600">Xác suất:</p>
                      <div className="space-y-1">
                        <div className="flex justify-between">
                          <span>Không có nguy cơ:</span>
                          <span>{(prediction.probability.no_risk * 100).toFixed(1)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Có nguy cơ:</span>
                          <span>{(prediction.probability.risk * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Chatbot */}
            <Card>
              <CardHeader>
                <CardTitle 
                  className="flex items-center gap-2 cursor-pointer"
                  onClick={() => setShowChat(!showChat)}
                >
                  <MessageCircle className="h-5 w-5" />
                  Chatbot tư vấn
                </CardTitle>
              </CardHeader>
              {showChat && (
                <CardContent>
                  <div className="space-y-4">
                    <div className="h-64 overflow-y-auto border rounded p-2 space-y-2">
                      {chatMessages.map((msg, index) => (
                        <div
                          key={index}
                          className={`p-2 rounded ${
                            msg.type === 'user' 
                              ? 'bg-blue-100 ml-4' 
                              : 'bg-gray-100 mr-4'
                          }`}
                        >
                          <p className="text-sm">{msg.message}</p>
                        </div>
                      ))}
                    </div>
                    <form onSubmit={handleChatSubmit} className="flex gap-2">
                      <Input
                        value={chatInput}
                        onChange={(e) => setChatInput(e.target.value)}
                        placeholder="Hỏi về nguy cơ đau tim..."
                        className="flex-1"
                      />
                      <Button type="submit">Gửi</Button>
                    </form>
                  </div>
                </CardContent>
              )}
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

