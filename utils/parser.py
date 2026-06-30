import json

def safe_json_parse(text: str, fallback_agent_name: str = "Agent"):
    """
    Parses JSON from Gemini's response.
    Handles cases where Gemini wraps output in ```json ... ``` blocks.
    Returns a dict or list depending on what Gemini returned.
    """
    # Clean up common formatting issues
    text = text.strip()
    
    # First try: direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Second try: strip markdown code fences
    try:
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                try:
                    return json.loads(part)
                except:
                    continue
    except:
        pass

    # Final fallback
    print(f"[{fallback_agent_name}] WARNING: Could not parse JSON.")
    print(f"[{fallback_agent_name}] Raw response: {text[:300]}")
    return {}