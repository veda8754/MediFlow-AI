from modules.response_generator import generate_patient_response

# Sample patient enquiry
enquiry = """
I have been waiting for three days
for confirmation of my appointment.
Nobody has contacted me.
"""

# Previously obtained AI classification
classification = {
    "category": "Appointment Booking",
    "sentiment": "Negative",
    "priority": "High",
    "requires_followup": True,
    "summary": "Patient has been waiting three days without contact regarding appointment confirmation."
}

print("\n===== AI CLASSIFICATION =====")

for key, value in classification.items():
    print(f"{key}: {value}")

# Generate response
print("\nGenerating AI response...")

try:
    reply = generate_patient_response(
        enquiry,
        classification
    )

    print("\n===== AI GENERATED RESPONSE =====")
    print(reply)

except Exception as e:
    print("\nResponse generation failed:")
    print(type(e).__name__, e)