from groq import Groq
import os

# Load API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Create client
client = Groq(api_key=GROQ_API_KEY)

# Make request
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Say hi"}]
)

print(response.choices[0].message.content)