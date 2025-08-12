import logging
from dotenv import load_dotenv
import os

load_dotenv()

# Logging configuration
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration API Google Custom Search
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")

# Path to Selenium WebDriver
SELENIUM_PATH = r"path"
