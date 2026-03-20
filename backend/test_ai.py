import google.generativeai as genai

genai.configure(api_key="AIzaSyAaBn7CkKwvFxJe3J5_GoSREDjfcpvrWQ4")

try:
    print("Testing gemini-2.0-flash...")
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("Say hello briefly")
    print("✅ SUCCESS! Response:", response.text[:100])
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__} - {str(e)[:300]}")

# Also try other model names
try:
    print("\nTesting gemini-pro...")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Say hello briefly")
    print("✅ SUCCESS with gemini-pro! Response:", response.text[:100])
except Exception as e:
    print(f"❌ ERROR with gemini-pro: {type(e).__name__} - {str(e)[:200]}")
