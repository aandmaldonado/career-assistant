import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def scrape_job_url(url: str) -> str:
    """
    Fetches the content of a URL and returns the visible text.
    Uses 'primp' to mimic a real browser and bypass 403 Forbidden errors.
    """
    logger.info(f"Scraping URL: {url}")
    
    # Try using primp (Browser Impersonation)
    try:
        import primp
        # Try mimicking a standard browser first
        client = primp.Client(impersonate="chrome_124", follow_redirects=True)
        response = client.get(url, timeout=15)
        response.raise_for_status()
        html_content = response.text
    except Exception as e:
        logger.warning(f"Primp chrome impersonation failed: {e}. Trying Googlebot fallback...")
        try:
             # Fallback: Pretend to be Googlebot (often allowed by WAFs)
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html_content = response.content
        except Exception as e2:
            logger.error(f"All scraping methods failed for {url}: {e2}")
            # Instead of crashing, return a helpful message so the user knows to paste text
            raise ValueError(f"Unable to access URL (Protected by WAF/Cloudflare). Please copy/paste the job description text manually.\nDetails: {e2}")

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove common non-content elements
    for element in soup(["script", "style", "nav", "footer", "header", "noscript", "iframe", "svg"]):
        element.extract()
        
    # Get text
    text = soup.get_text()
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text
