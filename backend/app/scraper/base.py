import requests
from bs4 import BeautifulSoup

class BaseScraper:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    }

    def get_soup(self, url: str):
        resp = requests.get(
            url,
            headers=self.headers,
            timeout=15
        )
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
