from langchain_tavily import TavilySearch 
from config.config import TAVILY_API_KEY

def perform_web_search(query):
    try:
        search = TavilySearch(
            tavily_api_key=TAVILY_API_KEY, 
            max_results=3
        )
        results = search.run(query)
        return results
    except Exception as e:
        return f"Search failed: {str(e)}"