from core.domain.interfaces import Scraper
from webdriver_manager import chrome
from RPA.Browser.Selenium import Selenium
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from enum import Enum


class AvailablesSections()


class DateRange(Enum):
    any_time = timedelta(days=365 * 1_000_000)
    past_24_hours = timedelta(hours=24)
    past_week = timedelta(weeks=1)
    past_month = timedelta(days=30)
    past_year = timedelta(days=365)


class SeleniumScraper(Scraper):
    def __init__(self) -> None:
        self.base_url = 'https://www.reuters.com/site-search/?query={}&section={}&offset=0&date={}'
        self.browser = Selenium()
        self.browser.open_available_browser(url=self.news_url, maximized=True, headless=False)
        self.available_section = Literal[]
        


    def __date_to_range(self, input_date: datetime) -> DateRange:
        now = datetime.now()
        
        if now - input_date <= DateRange.past_24_hours.value:
            return DateRange.past_24_hours
        elif now - input_date <= DateRange.past_week.value:
            return DateRange.past_week
        elif now - input_date <= DateRange.past_month.value:
            return DateRange.past_month
        elif now - input_date <= DateRange.past_year.value:
            return DateRange.past_year
        else:
            return DateRange.any_time

    def scrape_news(self, search_phrase: str, category: , months):

        

    # def scrape_news(self, search_phrase, category, months):