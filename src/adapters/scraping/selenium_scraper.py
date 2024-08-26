import logging
from datetime import date, datetime, timedelta
from enum import Enum
from typing import List, Optional
from uuid import uuid4
import undetected_chromedriver as uc
from robocorp.tasks import get_output_dir
from RPA.Browser.Selenium import ElementNotFound, Selenium
from RPA.HTTP import HTTP
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from core.domain.entities import NewsArticle
from core.domain.interfaces import Scraper


class Elements(Enum):
    SEARCH_TITLE = '//*[@id="main-content"]'
    ALL_OFFSET = "xpath:/html/body/div[1]/div[2]/div[2]/div/div[2]/div[3]/span"
    NEWS_LIST = "ul.search-results__list__2SxSK > li"
    NEWS_TITLE = "a[data-testid='Title']"
    NEWS_SECTION = "span[data-testid='Label']"
    NEWS_DATE = "time[data-testid='Text']"
    LINK = "a"
    IMAGE = "img"


class SeleniumScraper(Scraper):
    """
    A scraper class that uses Selenium to scrape news articles from Reuters based on a search phrase,
    date range, and section, and handles saving images locally.

    Attributes:
        offset (str): The URL parameter used for pagination.
        base_url (str): The base URL template for Reuters search.
        browser (Selenium): The Selenium browser instance.
        _driver (Optional[WebDriver]): The WebDriver instance, initialized lazily.
        _http (Optional[HTTP]): An HTTP client for downloading images, initialized lazily.

    Methods:
        driver: Property to initialize and get the Selenium WebDriver.
        http: Property to initialize and get the HTTP client.
        scrape_news: Scrapes news articles based on provided search parameters.
    """

    def __init__(self) -> None:
        self.offset = "offset={}"
        self.base_url = "https://www.reuters.com/site-search/?query={}&section={}&{}&date=any_time&sort=newest"
        self.browser = Selenium()
        self._driver = None
        self._http = None  # using another lib, like requests or urllib, because HTTP RPA slow download image

    @property
    def driver(self):
        """
        Initializes and returns the Selenium WebDriver with specific options if not already initialized.

        Returns:
            WebDriver: The initialized Selenium WebDriver instance.
        """
        if self._driver is None:
            chrome_options = Options()
            chrome_options.page_load_strategy = "eager"
            self._driver = uc.Chrome(options=chrome_options)
        return self._driver

    @property
    def http(self):
        """
        Initializes and returns the HTTP client for downloading images if not already initialized.

        Returns:
            HTTP: The initialized HTTP client instance.
        """
        if self._http is None:
            self._http = HTTP()
        return self._http

    def scrape_news(
        self,
        scrape_id: str,
        search_phrase: str,
        earliest_date: date,
        section: str = "all",
    ) -> Optional[List[NewsArticle]]:
        """
        Scrapes news articles from Reuters based on the provided search phrase, earliest date, and section.

        Args:
            scrape_id (str): The ID of the scrape process, used for organizing saved data.
            search_phrase (str): The phrase to search for in the news articles.
            earliest_date (date): The earliest date for filtering news articles.
            section (str, optional): The section of the news to search in. Defaults to "all".

        Returns:
            Optional[List[NewsArticle]]: A list of NewsArticle objects if scraping is successful, None otherwise.
        """
        logging.info(f"Search Phrase: {search_phrase}")
        logging.info(f"Section: {section}")

        query = "+".join(search_phrase.split())
        offset = self.offset.format(0)

        url = self.base_url.format(query, section, offset)

        # exploring captcha breaker
        browser_alias = "undetected_chrome"
        self.browser.register_driver(driver=self.driver, alias=browser_alias)
        self.browser.switch_browser(browser_alias)
        self.browser.set_selenium_implicit_wait(timedelta(seconds=50))
        self.browser.go_to(url=url)

        # exploring explict waits
        self.wait = WebDriverWait(self.browser.driver, 10)

        try:
            # exploring selenium wait with selenium RPA
            offset_element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, Elements.ALL_OFFSET.value.removeprefix("xpath:"))
                )
            )
        except TimeoutException:
            logging.error(f"No search result match the term: {search_phrase}")
            logging.warning(self.browser.get_source())
            self.browser.close_browser()
            return

        max_offset = int(offset_element.text.split()[-1])

        logging.info(f"Offset range: {max_offset//20}")

        news_articles = []
        break_scrape = False

        for offset in range(0, max_offset, 20):
            # exploring wait from RPAframework
            try:
                self.browser.wait_until_page_contains_element(
                    f"xpath:{Elements.SEARCH_TITLE.value}", 40
                )
            except TimeoutException:
                logging.error("Lazy page.")
                return

            news_list = self.browser.get_webelements(f"css:{Elements.NEWS_LIST.value}")
            total_height: int = self.browser.execute_javascript(
                "return document.body.scrollHeight"
            )
            scroll_height = total_height // len(news_list)
            scroll_coord = 0

            for i, news in enumerate(news_list):
                scroll_coord += scroll_height
                article_id = str(uuid4())
                self.browser.execute_javascript(
                    f"window.scrollBy(0, {scroll_coord*0.7});"
                )
                news_title = self.browser.get_webelement(
                    f"css:{Elements.NEWS_TITLE.value}", news
                )
                logging.info(f"Collecting {i}/{len(news_list)}: {news_title.text}")

                news_clickable = news.find_element(By.CSS_SELECTOR, Elements.LINK.value)
                news_url: str = news_clickable.get_attribute("href")
                news_url_splitted = news_url.split("-")
                news_date = "-".join(news_url_splitted[-3:]).removesuffix("/")
                news_date = datetime.strptime(news_date, "%Y-%m-%d").date()

                logging.info(
                    f"Comparing article date: {news_date} with earliest date: {earliest_date}"
                )
                if news_date < earliest_date:
                    break_scrape = True
                    logging.info("No more news in between selected date.")
                    break

                try:
                    article_section = self.browser.get_webelement(
                        f"css:{Elements.NEWS_SECTION.value}", news
                    ).text
                except ElementNotFound:
                    article_section = None

                logging.info(f"Saving thumbnail: {news_title}")

                image_path = get_output_dir() / f"results_{scrape_id}" / "thumbnails"
                image_path.mkdir(exist_ok=True, parents=True)

                # image_element = news.find_element(By.CSS_SELECTOR, Elements.IMAGE.value)
                # image_url = image_element.get_attribute("src")
                image_file = image_path / article_id
                image_file = image_file.with_suffix(".png")

                # self.http.download(image_url, image_file)

                article = NewsArticle(
                    article_id=article_id,
                    title=news_title.text,
                    date=news_date,
                    url=news_url,
                    image_path=str(image_file),
                    extracted_section=article_section,
                    selected_section=section,
                )

                news_articles.append(article)

            if not break_scrape:
                self.browser.execute_javascript("window.stop();")
                logging.info(f"Go to Offset: {offset}")
                self.browser.go_to(self.base_url.format(query, section, offset))
            else:
                logging.info(f"Finish Scrape in offset: {offset}")
                break

        self.browser.close_all_browsers()
        return news_articles
