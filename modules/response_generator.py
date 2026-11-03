from modules.gemini_client import generate_response
from utils.response_prompts import RESPONSE_PROMPT


def generate_patient_response(enquiry, classification):

    prompt = RESPONSE_PROMPT.format(
        enquiry=enquiry,
        category=classification["category"],
        sentiment=classification["sentiment"],
        priority=classification["priority"]
    )

    response = generate_response(prompt)

    return response.strip()