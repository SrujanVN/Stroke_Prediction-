import joblib
import pandas as pd
import numpy as np

try:
    print("Loading model...")
    model = joblib.load('stroke_model.pkl')
    print(f"Model Type: {type(model)}")
    
    if hasattr(model, 'get_params'):
        print(f"Model Params: {model.get_params()}")
    
    if hasattr(model, 'feature_importances_'):
        print("Feature Importances found.")
    
    if hasattr(model, 'coef_'):
        print("Coefficients found.")

except Exception as e:
    print(f"Error: {e}")
