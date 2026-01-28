import os
import google.generativeai as genai

# Set API key
os.environ['GOOGLE_GENAI_API_KEY'] = "AIzaSyCwiPGY5Shz2FEIRZBO7zpDEMK-6x74UPs"

# Configure genai
api_key = os.getenv('GOOGLE_GENAI_API_KEY')
genai.configure(api_key=api_key)

print("✅ Gemini configured")

try:
    # Create model
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Model created")
    
    # Generate response
    response = model.generate_content("What are the warning signs of a stroke? Keep it very brief.")
    print("\n✅ Response received:")
    print(response.text)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
