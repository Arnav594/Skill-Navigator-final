import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    print("Testing gemini-2.0-flash...")
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Say hello briefly")
    print("✅ SUCCESS! Response:", response.text[:100])
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__} - {str(e)[:300]}")

try:
    print("\nTesting gemini-pro...")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Say hello briefly")
    print("✅ SUCCESS with gemini-pro! Response:", response.text[:100])
except Exception as e:
    print(f"❌ ERROR with gemini-pro: {type(e).__name__} - {str(e)[:200]}")