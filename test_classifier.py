from modules.classifier import classify_enquiry

enquiry = """
I have been waiting for three days
for confirmation of my appointment.
Nobody has contacted me.
"""

result = classify_enquiry(enquiry)

print("\n===== MEDIFLOW AI CLASSIFICATION =====")

for key, value in result.items():
    print(f"{key}: {value}")