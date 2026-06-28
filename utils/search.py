import requests

def web_search(query: str, num_results: int = 5) -> list[str]:
    """
    Searches the web using DuckDuckGo's free instant answer API.
    Returns a list of text snippets relevant to the query.
    
    Why DuckDuckGo? It has a free, no-key-required API endpoint.
    Good enough for our agents to get real-world context.
    """
    try:
        # DuckDuckGo's instant answer endpoint
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        
        # AbstractText is a summary paragraph if available
        if data.get("AbstractText"):
            results.append(data["AbstractText"])
        
        # RelatedTopics are snippets about related subtopics
        for topic in data.get("RelatedTopics", [])[:num_results]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append(topic["Text"])
        
        # If we got nothing useful, return a fallback message
        if not results:
            results = [f"Limited search results found for: {query}. "
                      f"Gemini will use its training knowledge instead."]
        
        return results[:num_results]
    
    except Exception as e:
        # Never crash an agent because search failed
        # Return a fallback so the agent can still run using Gemini's knowledge
        return [f"Search temporarily unavailable. Using knowledge base for: {query}"]