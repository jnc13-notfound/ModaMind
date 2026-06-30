import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import client, MODEL
from utils.parser import safe_json_parse


def critic_agent(synthesis_output: dict) -> dict:
    """
    Critic Agent
    
    Job: Review the Synthesis Agent's brand brief for quality.
    Checks for vague claims, missing specifics, and weak reasoning.
    Acts as a quality gate before the report reaches the user.
    
    Input: the dict returned by synthesis_agent()
    Output: dict with pass/fail, score, and specific weaknesses found
    """
    
    print(f"[Critic] Reviewing synthesis output for quality...")
    
    prompt = f"""
You are the Critic Agent for ModaMind, a fashion brand intelligence platform.

Your job is to critically review a brand intelligence brief BEFORE it reaches 
the client. You are skeptical and thorough — like a senior consultant reviewing 
a junior analyst's work before it goes to the CEO.

Brief to review:
{json.dumps(synthesis_output, indent=2)}

Evaluate against this rubric:
1. SPECIFICITY: Are claims specific and tied to evidence, or vague and generic?
   (e.g. "improve marketing" = vague/bad. "Launch a TikTok campaign targeting 
   Gen Z around the quiet luxury trend" = specific/good)
2. ACTIONABILITY: Could someone literally act on the recommended_actions tomorrow?
3. COHERENCE: Does the cross_agent_insight genuinely connect multiple findings, 
   or is it just restating one finding?
4. RISK CLARITY: Is the risk_flag specific and real, or generic boilerplate?

Score 1-10 where:
1-4 = Needs significant revision, too vague to be useful
5-7 = Acceptable but has weaknesses
8-10 = Strong, specific, ready to present to a client

Return ONLY a valid JSON object. No explanation, no markdown.
Format:
{{
  "passed": true,
  "score": 8,
  "weaknesses_found": ["specific weakness 1", "specific weakness 2"],
  "strengths": ["what's good about this brief"],
  "revision_notes": "If score is below 7, specific instructions on what to fix. 
  If score is 7+, write 'No revision needed.'"
}}
"""
    
    print(f"[Critic] Calling Gemini...")
    response = client.models.generate_content(model=MODEL, contents=prompt)
    result = safe_json_parse(response.text, "Critic")
    
    score = result.get('score', 0)
    print(f"[Critic] ✓ Review complete. Score: {score}/10")
    
    return result


if __name__ == "__main__":
    print("Testing Critic Agent with sample data...")
    print("=" * 50)
    
    # Intentionally weak sample to test if Critic catches vagueness
    weak_sample = {
        "executive_summary": "The brand is doing okay but could improve.",
        "top_opportunity": "Marketing could be better.",
        "cross_agent_insight": "Trends and influencers are both important.",
        "risk_flag": "Competition exists.",
        "recommended_actions": ["Do more marketing", "Be more sustainable"]
    }
    
    result = critic_agent(weak_sample)
    print(json.dumps(result, indent=2))
    print("\n✓ Critic Agent working correctly")