# Websites Scraper

## Overview
This project allows you to:
1. Search websites using the **Google Custom Search API**.
2. Parse the found websites to extract:
   - Page title
   - Contact information (emails and phone numbers for Kazakhstan and Russia)
   - Domain
   - Creation/publication date (supports Russian month formats)
   - First 10 found hyperlinks
3. Save both raw search results and parsed website data into Excel files.

It uses:
- `google_api.py` — Wrapper for Google Custom Search API.
- `scraper.py` — Website parsing logic.
- `utils.py` — Helper functions for logging, date extraction, and domain parsing.
- `config.py` — Configuration settings (API keys, Selenium driver path).

## Installation

1. Set up Google API keys
    - Get an API key from [Google Cloud Console](https://console.cloud.google.com/)
    - Create a [Custom Search Engine](https://programmablesearchengine.google.com/)
    - Update config.py:
        ```
        GOOGLE_API_KEY = "your_api_key_here"
        GOOGLE_CX = "your_custom_search_engine_id_here"
        ```
2. Install ChromeDriver
    - Download [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads) matching your Chrome version.
    - Update SELENIUM_PATH in config.py to the correct path.

## Notes
1. Search Google using your query (query variable in main.py).
2. Emails and phone numbers are extracted from visible text on the page.
3. Supports both Russia (RU) and Kazakhstan (KZ) phone formats.
4. Dates are detected even with Russian month names in various grammatical cases.
5. Selenium is used as a fallback if requests parsing fails.