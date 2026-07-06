import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.config as cfg
from utils.config import REGION_CONTEXT
from utils.search import web_search
from utils.parser import safe_json_parse


def ethics_auditor_agent(brand_name: str) -> dict:
    """
    Ethics Auditor Agent
    
    Job: Verify a brand's sustainability and ethical claims.
    Finds contradictions between what the brand claims and what evidence shows.
    Input: brand name
    Output: dict with credibility score and findings
    """
    
    print(f"[Ethics Auditor] Auditing {brand_name}'s sustainability claims...")
    
    query1 = f"{brand_name} sustainability claims environmental commitments India 2024 2025"
    query2 = f"{brand_name} greenwashing controversy labor practices criticism India"
    query3 = f"{brand_name} ethical fashion certification supply chain India"
    
    results = (web_search(query1, num_results=3) + 
               web_search(query2, num_results=3) + 
               web_search(query3, num_results=2))
    
    search_context = "\n\n".join([f"Source {i+1}: {r}" 
                                   for i, r in enumerate(results)])
    
    prompt = f"""
You are the Ethics Auditor Agent for ModaMind, a fashion brand intelligence platform.

Your task: Investigate {brand_name}'s public sustainability and ethical claims, 
then cross-reference them with third-party evidence to identify contradictions.

Brand: {brand_name}

{REGION_CONTEXT}

Evidence gathered:
{search_context}

Look specifically for:
- Claims the brand makes that have no third-party verification
- Contradictions between brand messaging and reported behavior
- Missing certifications they should have if their claims are true
- Labor practice concerns vs. stated values

Credibility score guide: 1-3 = serious greenwashing, 4-6 = mixed/unverified, 
7-8 = mostly credible, 9-10 = highly verified

Return ONLY a valid JSON object. No explanation, no markdown.
Format:
{{
  "claims_found": ["claim 1", "claim 2", "claim 3"],
  "contradictions": ["contradiction 1", "contradiction 2"],
  "missing_verifications": ["what they claim but can't verify 1", "...2"],
  "credibility_score": 6,
  "credibility_label": "Mixed — some claims unverified",
  "recommendation": "Specific advice for the brand on improving ethical credibility"
}}
"""
    
    print(f"[Ethics Auditor] Calling Gemini...")
    response = cfg.client.models.generate_content(model=cfg.MODEL, contents=prompt)
    result = safe_json_parse(response.text, "Ethics Auditor")
    
    print(f"[Ethics Auditor] ✓ Audit complete. Credibility: {result.get('credibility_score', 'N/A')}/10")
    return result


if __name__ == "__main__":
    print("Testing Ethics Auditor Agent...")
    print("=" * 50)
    result = ethics_auditor_agent("Zara")
    print(json.dumps(result, indent=2))
    print("\n✓ Ethics Auditor Agent working correctly")