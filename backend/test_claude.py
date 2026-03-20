import anthropic

client = anthropic.Anthropic(api_key="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")  # paste your key here

response = client.messages.create(
    model="claude-haiku-20240307",
    max_tokens=10,
    messages=[{"role": "user", "content": "Say hi"}]
)

print(response.content[0].text)