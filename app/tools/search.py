from duckduckgo_search import DDGS
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def search_company_reputation(company_name: str, max_results: int = 5) -> str:
    """
    Searches for company reputation, reviews, and red flags using DuckDuckGo.
    Returns a summarized string of titles and snippets.
    """
    if not company_name:
        return ""
    
    queries = [
        f"{company_name} tech company reviews glassdoor reddit blind",
        f"{company_name} layoffs news",
        f"{company_name} work culture reviews"
    ]
    
    results_text = []
    
    try:
        with DDGS() as ddgs:
            for query in queries:
                logger.info(f"Searching for: {query}")
                try:
                    # Reverting to default region to ensure results. 'wt-wt' might be returning empty for niche queries.
                    results = list(ddgs.text(query, max_results=3))
                    if results:
                        results_text.append(f"--- Results for '{query}' ---")
                        for r in results:
                            results_text.append(f"- [{r.get('title')}]({r.get('href')}): {r.get('body')}")
                    else:
                        logger.warning(f"No results found for query: {query}")
                except Exception as e:
                    logger.error(f"Error searching for '{query}': {e}")
                    results_text.append(f"Error searching for '{query}': {str(e)}")
    except Exception as e:
        logger.error(f"Search error for {company_name}: {e}")
        return f"Error performing search: {str(e)}"

    return "\n".join(results_text)
