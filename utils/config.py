from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY_for_ModaMind")

if not api_key:
    raise ValueError("API_KEY_for_ModaMind not found. Check your .env file.")

# New SDK uses a Client object instead of genai.configure()
client = genai.Client(api_key=api_key)

# We don't create a model object here anymore.
# The new SDK calls client.models.generate_content() directly.
# We export the client and the model name as a string.
MODEL = "models/gemini-2.5-flash"