import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils.config as cfg
from utils.config import REGION_CONTEXT

# Maps the dropdown label to (the agent's role description, 
# the key in our result dict where its original findings live)
AGENT_PROFILES = {
    "Trend Scout": {
        "role": "You are the Trend Scout Agent. You specialize in fashion trend "
                "forecasting and identifying emerging market signals.",
        "data_key": "trends"
    },
    "Brand Analyst": {
        "role": "You are the Brand Analyst Agent. You specialize in brand positioning, "
                "competitive analysis, and identifying strategic gaps.",
        "data_key": "brand_analysis"
    },
    "Ethics Auditor": {
        "role": "You are the Ethics Auditor Agent. You specialize in sustainability "
                "claim verification and supply chain transparency.",
        "data_key": "ethics"
    },
    "Consumer Psychology": {
        "role": "You are the Consumer Psychology Agent. You specialize in explaining "
                "why marketing campaigns work using psychological frameworks like "
                "scarcity, identity signaling, and social proof.",
        "data_key": "psychology"
    },
    "Influencer Matcher": {
        "role": "You are the Influencer Matcher Agent. You specialize in identifying "
                "the right creator partnerships for fashion brands.",
        "data_key": "influencers"
    },
    "Synthesis": {
        "role": "You are the Synthesis Agent. You specialize in connecting insights "
                "across multiple data sources into one coherent brand strategy.",
        "data_key": "synthesis"
    },
    "Critic": {
        "role": "You are the Critic Agent. You specialize in evaluating the quality "
                "and specificity of strategic recommendations.",
        "data_key": "critic"
    },
    "Content": {
        "role": "You are the Content Agent. You specialize in writing campaign-ready "
                "marketing copy — captions, ad headlines, and brand storytelling.",
        "data_key": "content"
    }
}


def chat_with_agent(agent_name: str, user_message: str, 
                     chat_history: list, pipeline_state: dict) -> str:
    """
    Lets the user have a real conversation with ONE specific agent.
    
    The agent stays "in character" — it knows its own original findings 
    (pulled from pipeline_state) and responds as that specialist would, 
    not as a generic assistant.
    
    Why this matters architecturally: this is what makes the system feel 
    genuinely multi-agent and interactive, rather than "one big report 
    generator." The user can now go deeper with exactly the agent whose 
    expertise they need.
    """
    
    if pipeline_state is None:
        return "Please run the full pipeline first, then come back to chat with an agent."
    
    profile = AGENT_PROFILES[agent_name]
    role_description = profile["role"]
    original_findings = pipeline_state.get(profile["data_key"], {})
    
    # Build conversation history into the prompt so the agent 
    # remembers what was already discussed in this chat session
    history_text = ""
    for turn in chat_history:
        if turn["role"] == "user":
            history_text += f"User: {turn['content']}\n"
        else:
            history_text += f"You: {turn['content']}\n"
    
    prompt = f"""
{role_description}

Here are YOUR original findings from the brand analysis you performed:
{original_findings}

Conversation so far:
{history_text}

User's new message: {user_message}

Respond as this specialist agent. Stay focused on your area of expertise. 
If asked to revise or expand something (like a caption or recommendation), 
do so directly and concretely — don't just describe what you would do, 
actually do it.
"""
    
    response = cfg.client.models.generate_content(model=cfg.MODEL, contents=prompt)
    return response.text