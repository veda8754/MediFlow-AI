from modules.gemini_client import generate_response

prompt = """
You are an administrative AI assistant
for a healthcare clinic.

A patient asks:

"Do you provide online consultations?"

Generate a short, friendly and professional
response.

Do not provide medical advice.
Do not invent clinic policies or prices.
"""

response = generate_response(prompt)

print("\n===== MEDIFLOW AI TEST =====")
print(response)