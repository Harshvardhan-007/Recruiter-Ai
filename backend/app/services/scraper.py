import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
import re

async def fetch_search_results(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Executes a web search query via DuckDuckGo/Google HTML scrape
    to extract candidate profile URLs and snippets without needing paid proxies for MVP.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Using DuckDuckGo HTML endpoint for reliable, lightweight SERP retrieval
    url = f"https://html.duckduckgo.com/html/?q={httpx.URL(query).raw_path.decode()}"
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            candidates = []
            results = soup.find_all("a", class_="result__url", limit=max_results)
            snippets = soup.find_all("a", class_="result__snippet", limit=max_results)
            titles = soup.find_all("a", class_="result__title", limit=max_results)
            
            for i in range(min(len(results), max_results)):
                raw_url = results[i].get("href", "")
                # Clean DuckDuckGo redirect wrapper if present
                clean_url = raw_url.split("uddg=")[-1].split("&")[0] if "uddg=" in raw_url else raw_url
                
                title_text = titles[i].get_text(strip=True) if i < len(titles) else "Candidate Profile"
                snippet_text = snippets[i].get_text(strip=True) if i < len(snippets) else ""
                
                candidates.append({
                    "title": title_text,
                    "profile_url": clean_url,
                    "snippet": snippet_text,
                    "source": "Web Search"
                })
                
            return candidates
        except Exception as e:
            print(f"Scraping error: {e}")
            return []