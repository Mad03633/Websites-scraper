import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from charset_normalizer import from_bytes
import re
import phonenumbers
from urllib.parse import urljoin
import pandas as pd
from utils import log_error, extract_domain, extract_date
from config import SELENIUM_PATH

class WebScraper:
    def __init__(self):
        self.selenium_path = SELENIUM_PATH

    def parse_website(self, url):
        try:
            return self.parse_with_requests(url)
        except Exception as e:
            log_error(f"Requests failed for {url}: {e}")
            return self.parse_with_selenium(url)

    def parse_with_requests(self, url):
        ua = UserAgent()
        headers = {"User-Agent": ua.random}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            detected_encoding = from_bytes(response.content).best().encoding
            response.encoding = detected_encoding if detected_encoding else response.apparent_encoding

            soup = BeautifulSoup(response.text, "html.parser")
            return self._extract_data(soup, url)
        except requests.exceptions.RequestException as e:
            log_error(f"Request failed for {url}: {e}")
            return None

    def parse_with_selenium(self, url):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        service = Service(self.selenium_path)
        with webdriver.Chrome(service=service, options=options) as driver:
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                soup = BeautifulSoup(driver.page_source, "html.parser")
                return self._extract_data(soup, url)
            except Exception as e:
                log_error(f"Selenium failed for {url}: {e}")
                return None

    def _extract_data(self, soup, url):
        return {
            "URL": url,
            "Domain": extract_domain(url),
            "Title": self._extract_title(soup),
            "Contacts": self._extract_contacts(soup),
            "All_Links": self._extract_links(soup, url),
            "Creation_Date": self._extract_creation_date(soup)
        }

    @staticmethod
    def _extract_title(soup):
        elem = soup.find('title')
        return elem.text.strip() if elem else "Not found"

    @staticmethod
    def _extract_contacts(soup):
        text = soup.get_text()

        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)

        phone_candidates = re.findall(r'\+?\d{10,15}', text)
        phones = []

        for number in phone_candidates:
            try:
                parsed_number = phonenumbers.parse(number, "RU")
                if phonenumbers.is_valid_number(parsed_number):
                    phones.append(phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
            except phonenumbers.phonenumberutil.NumberParseException:
                continue

        contacts = emails + phones
        return "; ".join(contacts) if contacts else "Not found"

    @staticmethod
    def _extract_links(soup, base_url):
        links = {urljoin(base_url, link['href']) for link in soup.find_all('a', href=True)}
        return "; ".join(list(links)[:10]) if links else "No links found"

    @staticmethod
    def _extract_creation_date(soup):
        text = soup.get_text()
        return extract_date(text)

    @staticmethod
    def save_parsed_data(data, filename="parsed_websites_data.xlsx"):
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Parsed data saved to {filename}")