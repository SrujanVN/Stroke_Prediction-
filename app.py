from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import google.generativeai as genai
import os
import traceback

app = Flask(__name__)

# Load model and scaler
try:
    model = joblib.load('stroke_model.pkl')
    scaler = joblib.load('scaler.pkl')
except FileNotFoundError:
    print("Error: Model or scaler file not found. Make sure 'stroke_model.pkl' and 'scaler.pkl' are in the root directory.")
    model = scaler = None

# Configure Gemini
try:
    api_key = os.getenv('GOOGLE_GENAI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel('gemini-pro')
        print("Gemini API configured successfully")
    else:
        print("Warning: GOOGLE_GENAI_API_KEY environment variable not set")
        gemini_model = None
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    gemini_model = None

def process_form_data(form):
    """
    Processes form data, encodes it, and prepares it for the model.
    Returns a dictionary of raw values and a list of features for the model.
    """
    # Numerical features
    raw_values = {
        'age': float(form['age']),
        'hypertension': int(form['hypertension']),
        'heart_disease': int(form['heart_disease']),
        'avg_glucose_level': float(form['avg_glucose_level']),
        'bmi': float(form['bmi'])
    }

    # Categorical features
    gender = form['gender']
    ever_married = form['ever_married']
    work_type = form['work_type']
    residence_type = form['residence_type']
    smoking_status = form['smoking_status']

    # Add categorical to raw_values for feature importance logic
    raw_values['smoking_status'] = smoking_status
    raw_values['work_type'] = work_type
    raw_values['residence_type'] = residence_type

    # --- Encoding ---
    # Gender: Male, Other (Female is baseline)
    gender_male = 1 if gender == 'Male' else 0
    gender_other = 1 if gender == 'Other' else 0

    # Ever Married: Yes (No is baseline)
    ever_married_yes = 1 if ever_married == 'Yes' else 0

    # Work Type: Private, Self-employed, children, Never_worked (Govt_job is baseline)
    work_type_private = 1 if work_type == 'Private' else 0
    work_type_self_employed = 1 if work_type == 'Self-employed' else 0
    work_type_children = 1 if work_type == 'Children' else 0
    work_type_never_worked = 1 if work_type == 'Never worked' else 0

    # Residence Type: Urban (Rural is baseline)
    residence_type_urban = 1 if residence_type == 'Urban' else 0

    # Smoking Status: formerly smoked, never smoked, smokes (Unknown is baseline)
    smoking_formerly = 1 if smoking_status == 'formerly smoked' else 0
    smoking_never = 1 if smoking_status == 'never smoked' else 0
    smoking_smokes = 1 if smoking_status == 'smokes' else 0

    # Combine all features in the correct order for the model
    features = [
        raw_values['age'], raw_values['hypertension'], raw_values['heart_disease'], 
        raw_values['avg_glucose_level'], raw_values['bmi'],
        gender_male, gender_other, ever_married_yes,
        work_type_private, work_type_self_employed, work_type_children, work_type_never_worked,
        residence_type_urban,
        smoking_formerly, smoking_never, smoking_smokes
    ]
    
    return raw_values, features

def get_top_risk_factors(raw_values):
    """
    Identifies the top 3 risk factors based on the user's input.
    This is a simplified heuristic and not based on model feature importance.
    """
    factors = []
    
    # Age
    if raw_values['age'] > 60:
        factors.append({'name': 'Advanced Age', 'value': int(raw_values['age']), 'impact': 3})
    
    # Hypertension
    if raw_values['hypertension'] == 1:
        factors.append({'name': 'Hypertension', 'value': 'Yes', 'impact': 3})
        
    # Heart Disease
    if raw_values['heart_disease'] == 1:
        factors.append({'name': 'Heart Disease', 'value': 'Yes', 'impact': 3})
        
    # BMI
    if raw_values['bmi'] >= 30:
        factors.append({'name': 'High BMI', 'value': raw_values['bmi'], 'impact': 2})
    elif raw_values['bmi'] >= 25:
        factors.append({'name': 'Overweight', 'value': raw_values['bmi'], 'impact': 1})
        
    # Glucose Level
    if raw_values['avg_glucose_level'] > 140: # Often indicates hyperglycemia
        factors.append({'name': 'High Glucose', 'value': raw_values['avg_glucose_level'], 'impact': 2})
        
    # Smoking
    if raw_values['smoking_status'] == 'smokes':
        factors.append({'name': 'Smoking', 'value': 'Currently smokes', 'impact': 2})

    return sorted(factors, key=lambda x: x['impact'], reverse=True)[:3]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    if request.method == 'POST':
        if not model or not scaler:
            return "Model not loaded", 500
            
        raw_values, features = process_form_data(request.form)
        scaled_input = scaler.transform([features])
        
        # Get probability instead of just prediction
        probability = model.predict_proba(scaled_input)[0][1] # Probability of class 1 (stroke)
        prediction_val = 1 if probability >= 0.02 else 0 # Use a 2% threshold for "High Risk"
        result = 'High Risk of Stroke' if prediction_val == 1 else 'Low Risk of Stroke'

        # Get top risk factors
        risk_factors = get_top_risk_factors(raw_values)
        
        # If the request is AJAX, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'prediction': result, 
                'probability': round(probability * 100, 1), 
                'risk_factors': risk_factors
            })
        
        # Otherwise, render the template with the result
        return render_template('index.html', prediction=result)

    return render_template('index.html', prediction=None)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Fallback responses - comprehensive stroke knowledge base
        response_text = get_stroke_response(user_message)
        
        # If Gemini is available, try to use it for better responses
        if gemini_model and 'gemini' not in user_message:
            try:
                system_prompt = """You are a knowledgeable and compassionate AI health assistant specializing in stroke awareness, prevention, and education. 
Provide accurate, evidence-based information. Always emphasize this is not a substitute for professional medical advice. 
For emergencies, strongly recommend calling emergency services. Use the FAST acronym when discussing symptoms.
Keep responses concise but comprehensive.

User question: """
                gemini_response = gemini_model.generate_content(system_prompt + user_message)
                return jsonify({'response': gemini_response.text})
            except:
                pass  # Fall back to predefined responses
        
        return jsonify({'response': response_text})
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred processing your message'}), 500

def get_stroke_response(message):
    """Returns appropriate response based on user message keywords"""
    
    # Warning signs and symptoms
    if any(word in message for word in ['warning', 'sign', 'symptom', 'recognize', 'detect']):
        return """**Warning Signs of a Stroke (FAST)**

Remember **FAST**:
- **F**ace drooping - One side of the face droops or is numb
- **A**rm weakness - One arm is weak or numb  
- **S**peech difficulty - Speech is slurred or hard to understand
- **T**ime to call 911 - If you see ANY of these signs, call emergency services immediately!

**Other symptoms:**
- Sudden numbness or weakness in leg
- Sudden confusion or trouble understanding
- Sudden trouble seeing in one or both eyes
- Sudden severe headache with no known cause
- Sudden trouble walking or loss of balance

**This is a medical emergency! Call 911 immediately if you notice these symptoms.**"""

    # FAST acronym
    elif 'fast' in message:
        return """**FAST Acronym for Stroke Recognition:**

**F** - Face drooping (Ask the person to smile)
**A** - Arm weakness (Ask them to raise both arms)
**S** - Speech difficulty (Ask them to repeat a simple phrase)
**T** - Time to call 911 (Call immediately if any signs present)

**Time is critical!** Every minute counts. Call emergency services right away - don't wait to see if symptoms improve."""

    # Risk factors
    elif any(word in message for word in ['risk', 'factor', 'cause', 'likelihood']):
        return """**Common Stroke Risk Factors:**

**Controllable factors:**
- High blood pressure (hypertension) - #1 risk factor
- Smoking
- High cholesterol
- Diabetes
- Obesity/being overweight  
- Physical inactivity
- Poor diet
- Heavy alcohol use
- Atrial fibrillation (irregular heartbeat)

**Non-controllable factors:**
- Age (risk increases after 55)
- Family history of stroke
- Previous stroke or TIA
- Gender (varies by age)
- Race/ethnicity

**Good news:** 80% of strokes are preventable through lifestyle changes and managing medical conditions!"""

    # Prevention
    elif any(word in message for word in ['prevent', 'avoid', 'reduce', 'lower', 'decrease']):
        return """**How to Prevent a Stroke:**

**Manage health conditions:**
- Control blood pressure (keep below 120/80)
- Manage diabetes
- Treat atrial fibrillation
- Lower high cholesterol

**Healthy lifestyle:**
- Don't smoke (or quit if you do)
- Exercise regularly (30+ minutes/day)
- Maintain healthy weight (BMI under 25)
- Eat a balanced diet (fruits, vegetables, whole grains)
- Limit alcohol consumption
- Manage stress

**Regular checkups:**
- Visit your doctor regularly
- Know your numbers (BP, cholesterol, glucose)
- Take prescribed medications

**Remember:** Small changes can make a big difference!"""

    # Types of stroke
    elif any(word in message for word in ['type', 'kind', 'ischemic', 'hemorrhagic', 'tia']):
        return """**Types of Stroke:**

**1. Ischemic Stroke (87% of strokes)**
- Caused by a blood clot blocking blood flow to the brain
- Most common type
- Often treated with clot-busting drugs if caught early

**2. Hemorrhagic Stroke (13% of strokes)**
- Caused by a blood vessel rupturing in the brain
- Often due to high blood pressure or aneurysms
- More severe but less common

**3. TIA (Transient Ischemic Attack)**
- "Mini-stroke" - temporary blockage
- Symptoms resolve within 24 hours (usually minutes)
- **Warning sign!** 1 in 3 people who have a TIA will have a major stroke
- Seek immediate medical attention even if symptoms resolve!"""

    # Recovery and rehabilitation
    elif any(word in message for word in ['recover', 'rehab', 'after', 'treatment', 'therapy']):
        return """**Stroke Recovery and Rehabilitation:**

**Immediate treatment:**
- Clot-busting drugs (tPA) if ischemic stroke caught within 4.5 hours
- Surgery for some hemorrhagic strokes
- Time is critical!

**Rehabilitation includes:**
- Physical therapy (movement, balance, coordination)
- Occupational therapy (daily activities, adaptive techniques)
- Speech therapy (communication, swallowing)
- Cognitive therapy (memory, problem-solving)

**Recovery timeline:**
- Most improvement in first 3-6 months
- Recovery can continue for years
- Every person's recovery is different
- Dedication to rehabilitation is key

**Support:**
- Family involvement is crucial
- Support groups help emotional recovery
- Stay positive and patient"""

    # Emergency/when to call 911
    elif any(word in message for word in ['emergency', '911', 'hospital', 'help', 'urgent']):
        return """**CALL 911 IMMEDIATELY IF:**

- Face drooping
- Arm weakness  
- Speech difficulty
- Sudden severe headache
- Sudden trouble seeing
- Sudden trouble walking
- Any stroke symptoms!

**DO NOT:**
- Wait to see if symptoms improve
- Drive yourself to the hospital
- Take aspirin without medical guidance (can worsen hemorrhagic stroke)

**TIME MATTERS!**
- Every minute, 1.9 million brain cells die during a stroke
- Treatment is most effective within first few hours
- "Time is brain" - act immediately!

**This is a medical emergency. Call emergency services right away!**"""

    # Default response
    else:
        return """Hello! I'm your AI health assistant specializing in stroke awareness and prevention.

**I can help you with:**
- Warning signs and symptoms (ask about "FAST")
- Risk factors for stroke
- Prevention strategies
- Types of strokes (ischemic, hemorrhagic, TIA)
- Recovery and rehabilitation
- When to seek emergency care

**Common questions you can ask:**
- "What are the warning signs of a stroke?"
- "How can I prevent a stroke?"  
- "What is the FAST acronym?"
- "What are stroke risk factors?"
- "What should I do in a stroke emergency?"

**Important:** I provide general information only. I am NOT a substitute for professional medical advice. For symptoms or emergencies, call 911 immediately!

What would you like to know about stroke prevention or awareness?"""
if __name__ == '__main__':
    app.run(debug=True, port=5000)
