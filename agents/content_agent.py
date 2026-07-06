import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.config as cfg
from utils.config import REGION_CONTEXT
from utils.parser import safe_json_parse


def content_agent(brand_name: str, synthesis_output: dict, 
                   psychology_output: dict) -> dict:
    """
    Content Agent
    
    Job: Generate campaign-ready marketing copy based on the approved 
    brand brief and psychological insights.
    
    Input: brand name, synthesis dict (the approved brief), 
           psychology dict (so copy uses the right emotional triggers)
    Output: dict with captions, email subject, ad headlines, brand story
    
    This is the second-to-last agent in the pipeline — it takes 
    STRATEGY (from Synthesis) and turns it into ASSETS.
    """
    
    print(f"[Content] Generating campaign content for {brand_name}...")
    
    # Notice: NO web search here. This agent doesn't need new information — 
    # it needs to creatively apply what Synthesis and Psychology already found.
    # This is a "generation" agent, not a "research" agent.
    
    prompt = f"""
You are the Content Agent for ModaMind, a fashion brand intelligence platform.

Your task: Write campaign-ready marketing copy for {brand_name} based on the 
approved strategic brief below. The copy must specifically leverage the 
psychological triggers identified by the Consumer Psychology Agent — don't 
write generic copy, write copy designed to trigger the EXACT emotional 
response that was found to work for this brand.

{REGION_CONTEXT}

APPROVED BRAND BRIEF:
{json.dumps(synthesis_output, indent=2)}

PSYCHOLOGICAL INSIGHTS TO LEVERAGE:
{json.dumps(psychology_output, indent=2)}

Write:
1. THREE Instagram captions tied to the top_opportunity identified above. 
   Each should be in a distinct tone (e.g. one bold/edgy, one aspirational, 
   one community-focused). Include relevant hashtags.
2. ONE email subject line designed to drive opens using the primary 
   psychological trigger identified.
3. TWO ad headlines (under 10 words each) for paid social/display ads.
4. ONE brand story paragraph (3-4 sentences) that could open a campaign 
   landing page, weaving in the cultural context from the brief.

Return ONLY a valid JSON object. No explanation, no markdown.
Format:
{{
  "instagram_captions": [
    {{"tone": "Bold/Edgy", "caption": "...", "hashtags": "#... #... #..."}},
    {{"tone": "Aspirational", "caption": "...", "hashtags": "#... #... #..."}},
    {{"tone": "Community-focused", "caption": "...", "hashtags": "#... #... #..."}}
  ],
  "email_subject": "...",
  "ad_headlines": ["...", "..."],
  "brand_story": "..."
}}
"""
    
    print(f"[Content] Calling Gemini...")
    response = cfg.client.models.generate_content(model=cfg.MODEL, contents=prompt)
    result = safe_json_parse(response.text, "Content")
    
    print(f"[Content] ✓ Campaign content generated")
    return result


if __name__ == "__main__":
    print("Testing Content Agent with sample data...")
    print("=" * 50)
    
    # Using mock data again — same reasoning as Day 3's Synthesis/Critic tests:
    # we don't want to burn API quota re-running the whole pipeline just 
    # to test this one agent
    sample_synthesis = {
        "executive_summary": "Nike India needs localized streetwear positioning.",
        "top_opportunity": "Launch a 'Gully-Tech' streetwear capsule blending\n "
                           "global silhouettes with local typography, priced 4500-6500 INR.",
        "cross_agent_insight": "Sustainability messaging clashes with pricing gaps.",
        "risk_flag": "Labor practice concerns in Southern India factories.",
        "recommended_actions": ["Launch Gully-Tech capsule", "Audit supply chain"]
    }
    sample_psychology = {
        "why_it_worked": "Taps into identity signaling and rebellion.",
        "primary_trigger": "Identity signaling",
        "what_customers_felt": "Pride and self-expression",
        "sentiment_score": 8
    }
    
    result = content_agent("Nike", sample_synthesis, sample_psychology)
    print(json.dumps(result, indent=2))
    print("\n✓ Content Agent working correctly")