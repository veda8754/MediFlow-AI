import json
from modules.gemini_client import generate_response
from utils.combined_prompt import COMBINED_PROMPT


def classify_enquiry(enquiry):

    prompt = COMBINED_PROMPT.format(
        enquiry=enquiry
    )

    response = generate_response(prompt)

    # Remove markdown formatting if Gemini adds it
    response = response.strip()

    if response.startswith("```"):
        response = response.split("\n", 1)[1]
        response = response.rsplit("```", 1)[0].strip()

    result = json.loads(response)

    required_fields = [
        "category",
        "sentiment",
        "priority",
        "summary",
        "requires_followup",
        "suggested_response"
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"Missing field in Gemini response: {field}"
            )

    return result