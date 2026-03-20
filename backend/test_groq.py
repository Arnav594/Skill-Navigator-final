from groq import Groq

client = Groq(api_key="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")  # paste your key here

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",  # ✅ new, working,
    messages=[{"role": "user", "content": "Say hi"}]
)

print(response.choices[0].message.content)