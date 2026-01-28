import joblib
import numpy as np

# Load model and scaler
try:
    model = joblib.load('stroke_model.pkl')
    scaler = joblib.load('scaler.pkl')
    log = open('debug_output.txt', 'w')
    log.write("Model and scaler loaded successfully.\n")
except Exception as e:
    with open('debug_output.txt', 'w') as f:
        f.write(f"Error loading model/scaler: {e}\n")
    exit()

def test_prediction(age, hypertension, heart_disease, glucose, bmi, smoking='smokes'):
    # Encoding logic from app.py
    # Features order MUST match app.py:
    # 0: age, 1: hypertension, 2: heart_disease, 3: avg_glucose_level, 4: bmi,
    # 5: gender_male, 6: gender_other, 7: ever_married_yes,
    # 8: work_type_private, 9: work_type_self_employed, 10: work_type_children, 11: work_type_never_worked,
    # 12: residence_type_urban, 13: smoking_formerly, 14: smoking_never, 15: smoking_smokes
    
    features = [
        float(age), int(hypertension), int(heart_disease), float(glucose), float(bmi),
        1, 0, 1, # gender_male=1 (Male), gender_other=0, ever_married_yes=1 (Yes)
        1, 0, 0, 0, # work_type_private=1, others=0
        1, # residence_type_urban=1
        0, 0, 1 if smoking == 'smokes' else 0 # smoking_smokes=1
    ]
    
    scaled_input = scaler.transform([features])
    prob = model.predict_proba(scaled_input)[0][1]
    prediction = "High Risk" if prob >= 0.1 else "Low Risk"
    
    log.write(f"Inputs: Age={age}, HT={hypertension}, HD={heart_disease}, Glucose={glucose}, BMI={bmi}, Smoking={smoking}\n")
    log.write(f"Probability: {prob*100:.2f}% -> {prediction}\n")
    log.write("-" * 30 + "\n")

# Test scenarios
test_prediction(65, 1, 1, 160, 32, 'smokes') # The one I gave the user
test_prediction(75, 1, 1, 200, 35, 'smokes') # Older, higher glucose
test_prediction(82, 1, 1, 270, 40, 'smokes') # Very high risk
test_prediction(50, 0, 0, 100, 25, 'never smoked') # Normal

log.close()
print("Debug results written to debug_output.txt")
