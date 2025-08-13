from google_api import GoogleSearchAPI
from scraper import WebScraper
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def main():
    google_api = GoogleSearchAPI()
    scraper = WebScraper()

    query = "кибер мошенничество" # Input your query
    search_results = google_api.google_search(query, num_results=30)

    for result in search_results:
        result["Query"] = query

    google_api.save_results(search_results)

    urls = [result["link"] for result in search_results]

    with ThreadPoolExecutor(max_workers=5) as executor:
        parsed_data = list(tqdm(executor.map(scraper.parse_website, urls), total=len(urls)))

    for data in parsed_data:
        if data:
            data["Query"] = query

    scraper.save_parsed_data([data for data in parsed_data if data])

if __name__ == "__main__":
    main()