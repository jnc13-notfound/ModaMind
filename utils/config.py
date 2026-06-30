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
MODEL = "models/gemini-flash-latest"

# Shared regional weighting instruction — imported by all agents
REGION_CONTEXT = """
IMPORTANT REGIONAL FOCUS:
Weight your analysis 60% toward the Indian fashion market and 40% toward 
global/international markets. Prioritize Indian consumer behavior, Indian 
fashion trends, Indian brands and competitors, Indian price sensitivity, 
and Indian cultural context. Still include relevant global context, but 
Indian market relevance should be the primary lens.
"""