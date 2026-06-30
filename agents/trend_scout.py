import json
import sys
import os

# This lets Python find utils/ even when running from different directories
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import client, MODEL , REGION_CONTEXT
from utils.search import web_search
from utils.parser import safe_json_parse

def trend_scout_agent(brand_name: str, category: str) -> list[dict]:
    """
    Trend Scout Agent
    
    Job: Find 5 emerging trends relevant to this brand and category.
    Input: brand name (string), category (string)
    Output: list of 5 trend dictionaries
    
    This agent is FIRST in the pipeline. Its output feeds into
    Brand Analyst and Consumer Psychology agents.
    """
    
    print(f"[Trend Scout] Searching trends for {brand_name} in {category}...")
    
    # Step 1: Search for real trend data
    # We run two different searches to get broader coverage
    query1 = f"{brand_name} {category} fashion trends India 2025"
    query2 = f"emerging {category} trends consumer behavior India 2025"
    
    results1 = web_search(query1, num_results=4)
    results2 = web_search(query2, num_results=3)
    
    # Combine and format as a readable block for Gemini
    all_results = results1 + results2
    search_context = "\n\n".join([f"Source {i+1}: {r}" 
                                   for i, r in enumerate(all_results)])
    
    # Step 2: Build the prompt
    # Notice: we tell Gemini EXACTLY what format to return
    # "Return ONLY a JSON array" — this is critical
    # If you say "return JSON", Gemini might add explanation text around it
    # which breaks json.loads()
    prompt = f"""
You are the Trend Scout Agent for ModaMind, a professional brand intelligence platform.

Your task: Identify the top 5 emerging trends most relevant to the brand and category below.

Brand: {brand_name}
Category: {category}

{REGION_CONTEXT}

Real-world search data (use this as context, not as your only source):
{search_context}

Instructions:
- Think like a senior trend forecaster at a fashion consultancy
- Focus on trends that are EMERGING (not already mainstream)
- Each trend must be SPECIFIC to {category}, not generic
- Momentum score = how fast this trend is growing (1-10)
- Actionability = one concrete thing {brand_name} could do to capitalize

Return ONLY a valid JSON array. No introduction, no explanation, no markdown formatting.
Format:
[
  {{
    "trend_name": "...",
    "momentum_score": 8,
    "cultural_context": "Why this trend is happening culturally right now",
    "actionability": "Specific action {brand_name} should take"
  }}
]
"""
    
    # Step 3: Call Gemini
    print(f"[Trend Scout] Calling Gemini API...")
    response = client.models.generate_content(model=MODEL,
    contents=prompt)
    raw_text = response.text.strip()
    
    # Step 4: Parse the JSON
    # Gemini sometimes wraps its response in ```json ... ``` markdown blocks
    # We need to strip those before parsing
    parsed = safe_json_parse(raw_text, fallback_agent_name="Trend Scout")
    
    print(f"[Trend Scout] ✓ Found {len(parsed)} trends")
    return parsed


# Test block — only runs when you execute this file directly
# Does NOT run when imported by main.py
if __name__ == "__main__":
    print("Testing Trend Scout Agent...")
    print("=" * 50)
    
    result = trend_scout_agent("Nike", "sportswear")
    
    print("\nRaw output:")
    print(json.dumps(result, indent=2))
    
    print(f"\n✓ Agent returned {len(result)} trends")
    print("✓ Trend Scout Agent is working correctly")