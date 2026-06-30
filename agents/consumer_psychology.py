import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import client, MODEL
from utils.search import web_search
from utils.parser import safe_json_parse


def consumer_psychology_agent(brand_name: str, campaign_name: str) -> dict:
    """
    Consumer Psychology Agent
    
    Job: Explain WHY a fashion campaign worked (or failed) using psychology frameworks.
    Tells you what customers actually felt and what triggered their behavior.
    Input: brand name, campaign name or description
    Output: dict with psychology breakdown and sentiment analysis
    """
    
    print(f"[Consumer Psychology] Analyzing '{campaign_name}' by {brand_name}...")
    
    query1 = f"{brand_name} {campaign_name} campaign consumer reaction public response"
    query2 = f"why did {brand_name} {campaign_name} work viral marketing psychology"
    query3 = f"{brand_name} {campaign_name} customer sentiment review Reddit Twitter"
    
    results = (web_search(query1, num_results=3) +
               web_search(query2, num_results=3) +
               web_search(query3, num_results=2))
    
    search_context = "\n\n".join([f"Source {i+1}: {r}" 
                                   for i, r in enumerate(results)])
    
    prompt = f"""
You are the Consumer Psychology Agent for ModaMind, a fashion brand intelligence platform.

Your task: Analyze WHY the campaign below worked or failed using consumer psychology 
frameworks. Go beyond surface-level — explain the deep psychological mechanisms.

Brand: {brand_name}
Campaign: {campaign_name}

Evidence of consumer reactions:
{search_context}

Analyze through these FIVE psychological lenses:

1. SCARCITY / FOMO: Did limited availability, countdown timers, or exclusivity 
   drive urgency? How did this affect purchase behavior?

2. IDENTITY SIGNALING: Did consumers buy to express who they are or who they 
   want to be? What identity did this campaign let them perform?

3. SOCIAL PROOF: Did celebrity endorsements, influencer use, or crowd behavior 
   validate the purchase? How did seeing others buy affect individual decisions?

4. ASPIRATIONAL GAP: Did the campaign sell a lifestyle or future self rather than 
   a product? What aspiration did it tap into?

5. EMOTIONAL TRIGGER: What primary emotion did it activate — belonging, rebellion, 
   status, nostalgia, joy, empowerment? Was it positive or negative emotion?

Also answer: What did customers ACTUALLY feel — excitement, skepticism, FOMO, 
pride, disappointment? What was the dominant sentiment and why?

Return ONLY a valid JSON object. No explanation, no markdown.
Format:
{{
  "why_it_worked": "2-3 sentence summary of the core psychological reason",
  "primary_trigger": "The single most powerful psychological mechanism used",
  "psychology_breakdown": {{
    "scarcity_fomo": "Specific analysis for this campaign",
    "identity_signaling": "Specific analysis for this campaign",
    "social_proof": "Specific analysis for this campaign",
    "aspirational_gap": "Specific analysis for this campaign",
    "emotional_trigger": "Primary emotion + how it was activated"
  }},
  "what_customers_felt": "What the actual consumer emotional experience was",
  "sentiment_score": 8,
  "sentiment_label": "Strongly Positive",
  "key_lesson": "The one transferable lesson other brands should learn from this"
}}
"""
    
    print(f"[Consumer Psychology] Calling Gemini...")
    response = client.models.generate_content(model=MODEL, contents=prompt)
    result = safe_json_parse(response.text, "Consumer Psychology")
    
    print(f"[Consumer Psychology] ✓ Psychology analysis complete")
    print(f"[Consumer Psychology] Primary trigger: {result.get('primary_trigger', 'N/A')}")
    return result


if __name__ == "__main__":
    print("Testing Consumer Psychology Agent...")
    print("=" * 50)
    result = consumer_psychology_agent("Nike", "Just Do It 2024")
    print(json.dumps(result, indent=2))
    print("\n✓ Consumer Psychology Agent working correctly")