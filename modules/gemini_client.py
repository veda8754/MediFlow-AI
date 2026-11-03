import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Locate project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load API key
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

# Initialize Gemini with timeout
client = genai.Client(
    api_key=api_key,
    http_options={
        "timeout": 30000
    }
)


def generate_response(prompt):

    max_attempts = 3

    for attempt in range(max_attempts):

        try:
            print(f"Gemini request attempt {attempt + 1}...")

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            print("Gemini response received successfully!")

            return response.text

        except errors.ServerError as e:

            if e.code != 503:
                raise

            if attempt == max_attempts - 1:
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"Gemini unavailable. Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

