from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets of the top search results."""
    results = tavily.search(query=query,max_results=5)

    out = []

    for r in results["results"]:
        out.append(f"""
        Title: {r['title']}
        URL: {r['url']}
        Snippet: {r['content']}
        """)

    return "\n----\n".join(out)

print(web_search.invoke("what are the recent news of wars?"))


@tool
def scrape_url(url: str) -> str:
    """Scrape a single URL and return the main text content."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "footer", "header"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

print(scrape_url.invoke("https://www.cnbc.com/2026/06/12/uk-gdp-april-iran-war-growth.html"))