# 🧠 Stroke Risk Prediction System

A comprehensive AI-powered web application for predicting stroke risk and providing educational resources about stroke awareness, prevention, and emergency response.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Model Information](#model-information)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The **Stroke Risk Prediction System** is a machine learning-powered web application designed to:
- Assess individual stroke risk based on health and lifestyle factors
- Provide personalized risk insights and recommendations
- Offer an AI-powered chatbot for stroke education
- Help users understand warning signs and prevention strategies

This tool aims to increase stroke awareness and encourage preventive healthcare measures. **Important:** This is an educational tool and NOT a substitute for professional medical advice.

## 🎥 Live Demo

Check out the live demonstration of **STROKE PREDICTION POWERED BY MACHINE LEARNING** in action:

[![Watch the Demo](https://img.youtube.com/vi/LHUcyvJyzzo/0.jpg)](https://youtu.be/LHUcyvJyzzo)

[**Watch the Demo Video**](https://youtu.be/LHUcyvJyzzo)

A quick walkthrough of the project in action.

> **Note:** Since the project is not yet deployed, watch the video above to see the features in real-time.

## ✨ Features

### 🔍 Stroke Risk Assessment
- **Intelligent Prediction**: Machine learning model trained on stroke risk factors
- **Personalized Risk Score**: Percentage-based probability with risk classification
- **Key Risk Factors**: Identifies top 3 contributing factors for each individual
- **User-Friendly Interface**: Clean, responsive design for easy data input

### 🤖 AI Health Assistant
- **Gemini-Powered Chatbot**: Integrated with Google's Gemini API for intelligent responses
- **Comprehensive Knowledge Base**: Built-in responses for common stroke-related questions
- **Topics Covered**:
  - FAST acronym (stroke warning signs)
  - Risk factors and prevention strategies
  - Types of strokes (ischemic, hemorrhagic, TIA)
  - Emergency procedures
  - Recovery and rehabilitation

### 📊 Assessment Features
- Real-time prediction with AJAX support
- Dynamic risk factor visualization
- Detailed health metrics input form
- Responsive mobile-friendly design

## 🛠️ Technology Stack

**Backend:**
- **Flask** - Web framework
- **Scikit-learn** - Machine learning model
- **LightGBM** - Gradient boosting framework
- **Joblib** - Model serialization
- **Google Generative AI** - Chatbot intelligence

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive design
- AJAX for asynchronous requests

**Machine Learning:**
- LightGBM classifier
- Feature scaling with StandardScaler
- One-hot encoding for categorical features

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Google Gemini API key (optional, for enhanced chatbot)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SrujanVN/Stroke_Prediction-.git
   cd Stroke_Prediction-
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   # For enhanced chatbot functionality
   set GOOGLE_GENAI_API_KEY=your_api_key_here  # Windows
   export GOOGLE_GENAI_API_KEY=your_api_key_here  # macOS/Linux
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## 🚀 Usage

### Stroke Risk Assessment

1. Navigate to the **Assessment** page
2. Fill in the health information form:
   - **Demographics**: Age, Gender, Marital Status
   - **Medical History**: Hypertension, Heart Disease
   - **Health Metrics**: Average Glucose Level, BMI
   - **Lifestyle**: Work Type, Residence Type, Smoking Status
3. Click **Predict Risk**
4. View your personalized risk assessment:
   - Risk classification (High/Low Risk)
   - Probability percentage
   - Top 3 contributing risk factors

### AI Health Assistant

1. Navigate to the **Chatbot** page
2. Ask questions about stroke:
   - "What are the warning signs of a stroke?"
   - "How can I prevent a stroke?"
   - "What is the FAST acronym?"
   - "What should I do in a stroke emergency?"
3. Receive instant, evidence-based responses

## 📁 Project Structure

```
stroke_prediction/
│
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── stroke_model.pkl          # Trained ML model
├── scaler.pkl               # Feature scaler
├── features.pkl             # Feature list
│
├── templates/               # HTML templates
│   ├── home.html           # Landing page
│   ├── index.html          # Assessment page
│   └── chatbot.html        # Chatbot interface
│
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css       # Stylesheets
│   └── images/             # Image assets
│
└── README.md               # This file
```

## 🤖 Model Information

### Training Features
The model considers 16 features:

**Numerical:**
- Age
- Average Glucose Level
- BMI (Body Mass Index)

**Categorical (One-Hot Encoded):**
- Gender (Male, Female, Other)
- Hypertension (Yes/No)
- Heart Disease (Yes/No)
- Ever Married (Yes/No)
- Work Type (Private, Self-employed, Govt job, Children, Never worked)
- Residence Type (Urban/Rural)
- Smoking Status (smokes, formerly smoked, never smoked, unknown)

### Model Performance
- **Algorithm**: LightGBM Classifier
- **Risk Threshold**: 2% probability for high-risk classification
- **Preprocessing**: StandardScaler for feature normalization

### Key Risk Indicators
The system identifies major risk factors based on clinical thresholds:
- Advanced age (>60 years)
- Hypertension
- Heart disease
- High BMI (≥30)
- Elevated glucose levels (>140 mg/dL)
- Smoking status

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/assessment` | GET/POST | Risk assessment form and prediction |
| `/chatbot` | GET | AI chatbot interface |
| `/api/chat` | POST | Chatbot message endpoint |

### Example API Request

**Prediction Request:**
```javascript
fetch('/assessment', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest'
  },
  body: formData
})
```

**Chatbot Request:**
```javascript
fetch('/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ message: 'What is FAST?' })
})
```

## ⚠️ Important Disclaimer

**This application is for educational and informational purposes only.**

- NOT a substitute for professional medical advice, diagnosis, or treatment
- Always consult qualified healthcare providers for medical decisions
- In case of emergency (stroke symptoms), call 911 immediately
- Do not rely solely on this tool for health decisions

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Improvement
- Enhanced model training with larger datasets
- Additional risk visualization charts
- Multi-language support
- Mobile app development
- Integration with wearable health devices

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Srujan VN**
- GitHub: [@SrujanVN](https://github.com/SrujanVN)
- Repository: [Stroke_Prediction-](https://github.com/SrujanVN/Stroke_Prediction-)

## 🙏 Acknowledgments

- Dataset sources for model training
- Google Generative AI for chatbot capabilities
- Flask and Scikit-learn communities
- Healthcare professionals for domain expertise

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact via GitHub profile

---

**Remember: Time is Brain! 🧠⏰**  
*If you or someone you know experiences stroke symptoms, call emergency services immediately. Every minute counts!*

### FAST - Stroke Warning Signs
- **F**ace drooping
- **A**rm weakness
- **S**peech difficulty
- **T**ime to call 911