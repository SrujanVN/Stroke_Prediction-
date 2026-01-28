import os
from google import genai

# Set API key
os.environ['GOOGLE_GENAI_API_KEY'] = "AIzaSyCwiPGY5Shz2FEIRZBO7zpDEMK-6x74UPs"

# Initialize client
try:
    client = genai.Client(api_key=os.getenv('GOOGLE_GENAI_API_KEY'))
    print("✅ Client initialized")
    
    # Test generation
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",
        contents="What are the warning signs of a stroke? Keep it brief."
    )
    
    print("\n✅ Response received:")
    print(response.text)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
