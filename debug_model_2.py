import joblib
import numpy as np

# Load model and scaler
try:
    model = joblib.load('stroke_model.pkl')
    scaler = joblib.load('scaler.pkl')
    log = open('debug_output_2.txt', 'w')
    log.write("Model and scaler loaded successfully.\n")
except Exception as e:
    with open('debug_output_2.txt', 'w') as f:
        f.write(f"Error loading model/scaler: {e}\n")
    exit()

def test_prediction(age, hypertension, heart_disease, glucose, bmi, smoking='smokes'):
    features = [
        float(age), int(hypertension), int(heart_disease), float(glucose), float(bmi),
        1, 0, 1, # gender_male=1 (Male), gender_other=0, ever_married_yes=1 (Yes)
        1, 0, 0, 0, # work_type_private=1, others=0
        1, # residence_type_urban=1
        0, 0, 1 if smoking == 'smokes' else 0 # smoking_smokes=1
    ]
    
    scaled_input = scaler.transform([features])
    prob = model.predict_proba(scaled_input)[0][1]
    
    log.write(f"Inputs: Age={age}, HT={hypertension}, HD={heart_disease}, Glucose={glucose}, BMI={bmi}, Smoking={smoking}\n")
    log.write(f"Probability: {prob*100:.2f}%\n")
    log.write("-" * 30 + "\n")

# Test scenarios to find the 10% and 5% thresholds
test_prediction(78, 1, 1, 160, 32, 'smokes')
test_prediction(80, 1, 1, 160, 32, 'smokes')
test_prediction(80, 1, 1, 200, 32, 'smokes')
test_prediction(75, 1, 1, 250, 35, 'smokes')
test_prediction(60, 1, 1, 250, 35, 'smokes')

log.close()
