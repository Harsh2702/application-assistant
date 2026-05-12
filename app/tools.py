import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import PyPDF2
import os
from app.config import TAVILY_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

# cache so CV is only read once per session
_cv_cache = None

def scrape_job_posting(url: str) -> dict:
    """Scrapes a job posting URL and returns the text content."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # remove noise
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # trim to avoid token overload
        text = text[:5000]

        return {"success": True, "content": text, "url": url}
    except Exception as e:
        return {"success": False, "content": str(e), "url": url}


def search_company_info(company_name: str) -> str:
    """Searches web for company info, culture and tech stack."""
    try:
        results = tavily.search(
            query=f"{company_name} company culture tech stack engineering",
            max_results=5
        )
        combined = "\n\n".join(
            f"Source: {r['url']}\n{r['content']}"
            for r in results["results"]
        )
        return combined[:4000]
    except Exception as e:
        return f"Search failed: {str(e)}"


def read_cv(cv_path: str) -> str:
    """Reads CV PDF once and caches it for the session."""
    global _cv_cache

    if _cv_cache:
        return _cv_cache

    if not os.path.exists(cv_path):
        return "CV file not found. Please check the path."

    try:
        text = ""
        with open(cv_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""

        _cv_cache = text.strip()
        return _cv_cache
    except Exception as e:
        return f"Failed to read CV: {str(e)}"

