import json
from agents.trend_scout import trend_scout_agent
from agents.brand_analyst import brand_analyst_agent
from agents.ethics_auditor import ethics_auditor_agent
from agents.consumer_psychology import consumer_psychology_agent
from agents.influencer_matcher import influencer_matcher_agent
from agents.synthesis_agent import synthesis_agent
from agents.critic_agent import critic_agent
from agents.content_agent import content_agent
from agents.report_agent import report_agent


def run_pipeline(brand_name: str, category: str, campaign_name: str,
                  competitors: list[str], target_audience: str,selected_model: str = None) -> dict:
    """
    The Orchestrator — runs all 7 agents in sequence, passing each 
    agent's output to the next as needed (A2A handoff).
    
    This function IS the multi-agent system. Everything before this 
    was building the parts. This assembles them.
    """
    
    print("\n" + "=" * 60)
    print(f"  MODAMIND PIPELINE STARTING — Brand: {brand_name}")
    print("=" * 60 + "\n")

    # Override model if user selected a specific one from the UI
    if selected_model:
        import utils.config as cfg
        cfg.MODEL = selected_model

    # If no competitors provided, let the Brand Analyst agent
    # find them itself — we pass a placeholder that tells Gemini to research
    if not competitors or competitors == ["a leading competitor"]:
        competitors = ["[Research and identify the top 3 competitors yourself based on the brand and category]"]
    
    # STAGE 1: Run the 5 specialist agents
    # In a more advanced version these could run in parallel (we'll 
    # discuss this in Day 5), but for now sequential is simpler to 
    # debug and perfectly fine for a 5-6 day capstone timeline
    
    trends = trend_scout_agent(brand_name, category)
    
    brand_analysis = brand_analyst_agent(brand_name, competitors)
    
    ethics = ethics_auditor_agent(brand_name)
    
    psychology = consumer_psychology_agent(brand_name, campaign_name)
    
    influencers = influencer_matcher_agent(brand_name, category, target_audience)
    
    # STAGE 2: Synthesis Agent merges all 5 outputs
    # THIS is the A2A handoff — 5 agents' outputs flow into ONE function call
    synthesis = synthesis_agent(brand_name, trends, brand_analysis, 
                                  ethics, psychology, influencers)
    
    # STAGE 3: Critic Agent reviews the synthesis
    critic_result = critic_agent(synthesis)
    
    # STAGE 4: The revision loop
    # If the Critic fails the brief, we ask Synthesis to try again
    # with the Critic's specific feedback included
    if not critic_result.get('passed', True) and critic_result.get('score', 10) < 7:
        print("\n[Orchestrator] Critic flagged issues. Requesting revision...\n")
        synthesis = revise_synthesis(brand_name, trends, brand_analysis, 
                                       ethics, psychology, influencers, 
                                       critic_result)
        # Re-check with critic one more time
        critic_result = critic_agent(synthesis)
     # STAGE 5: Content Agent generates campaign-ready copy
    content = content_agent(brand_name, synthesis, psychology)
    
    # STAGE 6: Report Agent compiles everything into the final document
    final_report = report_agent(
        brand_name, trends, brand_analysis, ethics, 
        psychology, influencers, synthesis, critic_result, content
    )

    print("\n" + "=" * 60)
    print(f"  PIPELINE COMPLETE — Final Critic Score: {critic_result.get('score')}/10")
    print("=" * 60 + "\n")
    
    # Return everything — Day 4's Content and Report agents will need 
    # all of this, not just the synthesis
    return {
        "brand_name": brand_name,
        "trends": trends,
        "brand_analysis": brand_analysis,
        "ethics": ethics,
        "psychology": psychology,
        "influencers": influencers,
        "synthesis": synthesis,
        "critic": critic_result,
        "content": content,
        "report": final_report
    }


def revise_synthesis(brand_name, trends, brand_analysis, ethics, 
                      psychology, influencers, critic_feedback):
    """
    Calls the Synthesis Agent again, but this time the Critic's 
    feedback is injected so Gemini knows specifically what to fix.
    
    This is the actual REVISION LOOP — not just a retry, but a 
    retry with specific corrective instructions. This is what 
    makes the self-critique loop genuinely agentic.
    """
    from utils.config import client, MODEL
    from utils.parser import safe_json_parse
    
    revision_notes = critic_feedback.get('revision_notes', '')
    weaknesses = critic_feedback.get('weaknesses_found', [])
    
    prompt = f"""
You previously wrote a brand brief for {brand_name} that was reviewed and found 
to have these weaknesses:

WEAKNESSES: {', '.join(weaknesses)}
SPECIFIC REVISION NOTES: {revision_notes}

Rewrite the brief addressing these issues directly. Be more specific and 
evidence-based this time.

Original data to work from:
TRENDS: {json.dumps(trends)}
BRAND ANALYSIS: {json.dumps(brand_analysis)}
ETHICS: {json.dumps(ethics)}
PSYCHOLOGY: {json.dumps(psychology)}
INFLUENCERS: {json.dumps(influencers)}

Return ONLY a valid JSON object in this exact format:
{{
  "executive_summary": "...",
  "top_opportunity": "...",
  "cross_agent_insight": "...",
  "risk_flag": "...",
  "recommended_actions": ["...", "...", "...", "..."]
}}
"""
    
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return safe_json_parse(response.text, "Synthesis Revision")


if __name__ == "__main__":
    # First full end-to-end test of the entire pipeline
    result = run_pipeline(
        brand_name="Nike",
        category="sportswear",
        campaign_name="Just Do It 2024",
        competitors=["Adidas", "Puma", "New Balance"],
        target_audience="Gen Z fitness enthusiasts in India"
    )
    
    print("\n\nFINAL SYNTHESIS OUTPUT:")
    print(json.dumps(result['synthesis'], indent=2))