import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import client, MODEL
from utils.search import web_search
from utils.parser import safe_json_parse


def influencer_matcher_agent(brand_name: str, category: str, 
                               target_audience: str) -> dict:
    """
    Influencer Matcher Agent
    
    Job: Find 5 influencers that genuinely fit the brand's aesthetic,
    audience, and values. Goes beyond follower count to find authentic fit.
    Input: brand name, category, target audience description
    Output: dict with shortlist of 5 influencers with fit scores
    """
    
    print(f"[Influencer Matcher] Finding influencers for {brand_name}...")
    
    query1 = f"top fashion influencers {category} {target_audience} Instagram TikTok 2025"
    query2 = f"{brand_name} brand ambassador influencer collaboration fit aesthetic"
    query3 = f"best {category} content creators authentic engagement {target_audience}"
    
    results = (web_search(query1, num_results=4) +
               web_search(query2, num_results=2) +
               web_search(query3, num_results=2))
    
    search_context = "\n\n".join([f"Source {i+1}: {r}" 
                                   for i, r in enumerate(results)])
    
    prompt = f"""
You are the Influencer Matcher Agent for ModaMind, a fashion brand intelligence platform.

Your task: Recommend 5 real influencers who would be an authentic, strategic fit 
for this brand. Focus on genuine aesthetic and audience alignment, not just follower count.

Brand: {brand_name}
Category: {category}
Target audience: {target_audience}

Context:
{search_context}

For each influencer consider:
- Does their visual aesthetic match the brand?
- Does their audience overlap with the brand's target customer?
- Have they worked with similar (not competing) brands?
- What collaboration format makes sense for them?

Collaboration formats: sponsored post, brand ambassador, product collab, 
event appearance, content series, affiliate partnership

Fit score: 1-10 (10 = perfect match on aesthetic + audience + values)

Return ONLY a valid JSON object. No explanation, no markdown.
Format:
{{
  "shortlist": [
    {{
      "name": "Full Name or Handle",
      "platform": "Instagram / TikTok / Both",
      "follower_tier": "Nano/Micro/Mid/Macro/Mega",
      "why_they_fit": "Specific reason tied to brand identity",
      "audience_overlap": "Description of their audience vs brand's target",
      "collaboration_format": "Recommended format and why",
      "fit_score": 8
    }}
  ],
  "strategy_note": "Overall influencer strategy recommendation for {brand_name}"
}}
"""
    
    print(f"[Influencer Matcher] Calling Gemini...")
    response = client.models.generate_content(model=MODEL, contents=prompt)
    result = safe_json_parse(response.text, "Influencer Matcher")
    
    count = len(result.get('shortlist', []))
    print(f"[Influencer Matcher] ✓ Found {count} influencer matches")
    return result


if __name__ == "__main__":
    print("Testing Influencer Matcher Agent...")
    print("=" * 50)
    result = influencer_matcher_agent(
        "Nike", 
        "sportswear", 
        "Gen Z fitness enthusiasts aged 18-25"
    )
    print(json.dumps(result, indent=2))
    print("\n✓ Influencer Matcher Agent working correctly")