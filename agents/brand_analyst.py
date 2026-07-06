import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.config as cfg
from utils.config import REGION_CONTEXT

from utils.search import web_search
from utils.parser import safe_json_parse


def brand_analyst_agent(brand_name: str, competitors: list[str]) -> dict:
    """
    Brand Analyst Agent
    
    Job: Analyze a brand's current positioning and find gaps vs competitors.
    Input: brand name, list of competitor names
    Output: dict with positioning analysis and opportunity summary
    """
    
    print(f"[Brand Analyst] Analyzing {brand_name} vs {', '.join(competitors)}...")
    
    query1 = f"{brand_name} brand positioning marketing strategy India 2025"
    query2 = f"{' vs '.join(competitors)} brand comparison {brand_name} India market position"
    
    results1 = web_search(query1, num_results=4)
    results2 = web_search(query2, num_results=3)
    
    search_context = "\n\n".join([f"Source {i+1}: {r}" 
                                   for i, r in enumerate(results1 + results2)])
    
    prompt = f"""
You are the Brand Analyst Agent for ModaMind, a fashion brand intelligence platform.

Your task: Analyze {brand_name}'s current brand positioning and identify strategic gaps 
compared to its competitors.

Brand: {brand_name}
Competitors: {', '.join(competitors)}

{REGION_CONTEXT}

Real-world context:
{search_context}

Think like a senior brand strategist. Be specific — avoid vague statements like 
"improve brand awareness." Every point must be actionable.

Return ONLY a valid JSON object. No explanation, no markdown.
Format:
{{
  "current_positioning": "One paragraph describing how {brand_name} is currently positioned",
  "strengths": ["specific strength 1", "specific strength 2", "specific strength 3"],
  "gaps": ["specific gap 1", "specific gap 2", "specific gap 3"],
  "competitor_advantages": ["what competitor X does better", "what competitor Y does better"],
  "opportunity_summary": "One paragraph: the single biggest brand opportunity right now"
}}
"""
    
    print(f"[Brand Analyst] Calling Gemini...")
    response = cfg.client.models.generate_content(model=cfg.MODEL, contents=prompt)
    result = safe_json_parse(response.text, "Brand Analyst")
    
    print(f"[Brand Analyst] ✓ Analysis complete")
    return result


if __name__ == "__main__":
    print("Testing Brand Analyst Agent...")
    print("=" * 50)
    result = brand_analyst_agent("Nike", ["Adidas", "Puma", "New Balance"])
    print(json.dumps(result, indent=2))
    print("\n✓ Brand Analyst Agent working correctly")