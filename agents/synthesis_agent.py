import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import client, MODEL, REGION_CONTEXT
from utils.parser import safe_json_parse


def synthesis_agent(brand_name: str, trends: list, brand_analysis: dict, 
                     ethics: dict, psychology: dict, influencers: dict) -> dict:
    """
    Synthesis Agent
    
    Job: Merge outputs from 5 specialist agents into one coherent brand brief.
    Find CROSS-AGENT insights — connections between trend data, brand gaps, 
    and influencer matches that no single agent could see alone.
    
    Input: outputs from all 5 specialist agents (as Python dicts/lists)
    Output: dict with executive summary and unified recommendations
    
    This is the A2A handoff point — every specialist agent's output 
    flows INTO this one function as structured data.
    """
    
    print(f"[Synthesis] Merging insights for {brand_name}...")
    
    # We don't search the web here — this agent only REASONS over 
    # what the other 5 agents already found. No new information, 
    # just connecting existing dots. This is what makes it "synthesis"
    # rather than "research."
    
    prompt = f"""
You are the Synthesis Agent for ModaMind, a fashion brand intelligence platform.

You have received structured findings from 5 specialist agents who each analyzed 
ONE dimension of the brand {brand_name}. Your job is to merge their findings into 
one coherent, strategic brand brief.

{REGION_CONTEXT}

=== TREND SCOUT FINDINGS ===
{json.dumps(trends, indent=2)}

=== BRAND ANALYST FINDINGS ===
{json.dumps(brand_analysis, indent=2)}

=== ETHICS AUDITOR FINDINGS ===
{json.dumps(ethics, indent=2)}

=== CONSUMER PSYCHOLOGY FINDINGS ===
{json.dumps(psychology, indent=2)}

=== INFLUENCER MATCHER FINDINGS ===
{json.dumps(influencers, indent=2)}

Your tasks:
1. Write an executive summary that captures the brand's current situation in 3-4 sentences
2. Identify the SINGLE biggest opportunity — ideally one that connects findings from 
   multiple agents (e.g. a trend that fits a brand gap AND has a matched influencer 
   who already represents that trend)
3. Identify ONE specific cross-agent insight — something only visible by looking 
   at multiple findings together, not visible from any single agent's report alone
4. Flag the single biggest risk the brand should be aware of
5. Write 4 specific, prioritized recommended actions

Be specific. Reference actual findings from above, not generic advice.
This insight must name a SPECIFIC trend, gap, or influencer from the data above — not a generic statement.
Return ONLY a valid JSON object. No explanation, no markdown.
Format:
{{
  "executive_summary": "3-4 sentence summary of {brand_name}'s current situation",
  "top_opportunity": "The single biggest opportunity, citing specific findings",
  "cross_agent_insight": "A connection between 2+ agent findings that's only visible 
  by looking at everything together",
  "risk_flag": "The most important risk or weakness to address",
  "recommended_actions": [
    "Specific action 1",
    "Specific action 2", 
    "Specific action 3",
    "Specific action 4"
  ]
}}
"""
    
    print(f"[Synthesis] Calling Gemini...")
    response = client.models.generate_content(model=MODEL, contents=prompt)
    result = safe_json_parse(response.text, "Synthesis")
    
    print(f"[Synthesis] ✓ Brand brief synthesized")
    return result


if __name__ == "__main__":
    # For isolated testing, we use FAKE sample data instead of running 
    # all 5 agents again (that would waste API quota every time you test this file)
    print("Testing Synthesis Agent with sample data...")
    print("=" * 50)
    
    sample_trends = [
        {"trend_name": "Quiet Luxury", "momentum_score": 8, 
         "cultural_context": "Post-recession minimalism in India", 
         "actionability": "Launch a minimal capsule line"}
    ]
    sample_brand = {
        "current_positioning": "Performance-focused sportswear brand",
        "strengths": ["Strong athlete endorsements", "Wide retail presence"],
        "gaps": ["Weak in lifestyle/casual segment", "No size-inclusive line"],
        "competitor_advantages": ["Competitor X dominates casualwear"],
        "opportunity_summary": "Expand into athleisure crossover"
    }
    sample_ethics = {
        "credibility_score": 6,
        "credibility_label": "Mixed",
        "recommendation": "Get third-party certification"
    }
    sample_psychology = {
        "why_it_worked": "Tapped into identity signaling for Gen Z",
        "primary_trigger": "Identity signaling",
        "sentiment_score": 8
    }
    sample_influencers = {
        "shortlist": [
            {"name": "Sample Creator", "region": "India", "fit_score": 8}
        ]
    }
    
    result = synthesis_agent("Nike", sample_trends, sample_brand, 
                              sample_ethics, sample_psychology, sample_influencers)
    print(json.dumps(result, indent=2))
    print("\n✓ Synthesis Agent working correctly")