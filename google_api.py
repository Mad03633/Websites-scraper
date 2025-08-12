import requests
import time
import random
import pandas as pd
from utils import log_error
from config import GOOGLE_API_KEY, GOOGLE_CX

class GoogleSearchAPI:
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
        self.cx = GOOGLE_CX

    def google_search(self, query, num_results=30):
        search_results = []
        url_template = (
            "https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}&start={start}"
        )
        for start in range(1, num_results, 10):
            url = url_template.format(query=query, api_key=self.api_key, cx=self.cx, start=start)
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                items = data.get("items", [])
                for item in items:
                    search_results.append({"title": item.get("title"), "link": item.get("link")})
                time.sleep(random.uniform(1, 3))
            except requests.exceptions.RequestException as e:
                log_error(f"Error during API request: {e}")
                break
        return search_results

    def save_results(self, results, filename="found_websites_api.xlsx"):
        df = pd.DataFrame(results)
        df.to_excel(filename, index=False)
        print(f"Results saved to {filename}")