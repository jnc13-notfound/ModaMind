from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY_for_ModaMind")

if not api_key:
    raise ValueError("API_KEY_for_ModaMind not found. Check your .env file.")

client = genai.Client(api_key=api_key)

# Primary model
MODEL = "models/gemini-flash-latest"

# Fallback models — used when primary quota is exhausted
# User can switch between these in the UI
AVAILABLE_MODELS = {
    "Gemini Flash (Latest)": "models/gemini-flash-latest",
    "Gemini 2.0 Flash": "models/gemini-2.0-flash",
    "Gemini 2.5 Flash": "models/gemini-2.5-flash",
    "Gemini 2.0 Flash Lite": "models/gemini-2.0-flash-lite",
    "Gemini 2.5 Flash Lite": "models/gemini-2.5-flash-lite",
}

REGION_CONTEXT = """
IMPORTANT REGIONAL FOCUS:
Weight your analysis 60% toward the Indian fashion market and 40% toward 
global/international markets. Prioritize Indian consumer behavior, Indian 
fashion trends, Indian brands and competitors, Indian price sensitivity, 
and Indian cultural context. Still include relevant global context, but 
Indian market relevance should be the primary lens.
"""