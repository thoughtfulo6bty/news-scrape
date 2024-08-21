from core.domain.interfaces import Scraper
from core.domain.entities import NewsArticle
from webdriver_manager import chrome
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from pathlib import Path
from robocorp.tasks import get_output_dir
from uuid import uuid4
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from typing import Literal
from enum import Enum


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Elements(Enum):
    SEARCH_TITLE = "h1[data-testid='Heading']"
    ALL_OFFSET = 'xpath:/html/body/div[1]/div[2]/div[2]/div/div[2]/div[3]/span'
    NEWS_LIST = 'ul.search-results__list__2SxSK > li'
    NEWS_TITLE = "a[data-testid='Title']"
    NEWS_SECTION = "span[data-testid='Label']"
    NEWS_DATE = "time[data-testid='Text']"
    LINK = 'a'
    IMAGE = 'img'


class SeleniumScraper(Scraper):
    def __init__(self) -> None:
        self.offset = 'offset={}'
        self.base_url = 'https://www.reuters.com/site-search/?query={}&section={}&{}&date=any_time'
        self.browser = Selenium()
        self.http = HTTP()

        # TODO: remove mock
        # self.image_path = get_output_dir() / 'thumbnails'
        self.image_path = Path('thumbnails')
        self.image_path.mkdir(exist_ok=True)



    def get_news_datails():
        pass


    def scrape_news(self, search_phrase: str,
                    section: Literal['all', 'world', 'business', 'legal', 
                                     'markets', 'breakingviews', 'technology', 
                                     'sustainability', 'science', 'sports', 'lifestyle', ] = 'all'):
        
        logging.info(f'Search Phrase: {search_phrase}')
        logging.info(f'Section: {section}')


        query =  '+'.join(search_phrase.split())
        offset = self.offset.format(0)

        url = self.base_url.format(query, section, offset)
        self.browser.open_available_browser(url=url, maximized=True, headless=False, options={'capabilities': {"pageLoadStrategy": "eager"}})    
        self.wait = WebDriverWait(self.browser.driver, 10)
        

        try:
            offset_element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, Elements.ALL_OFFSET.value.removeprefix('xpath:'))
                )
            )
        except TimeoutException:
            logging.error(f'No search result match the term: {search_phrase}')
            self.browser.close_browser()
            return
        
        max_offset = int(offset_element.text.split()[-1])
        offsets = range(0, max_offset, 20)

        logging.info(f'Offset range: {max_offset//20}')

        news_articles = []

        for offset in offsets:
            news_list = self.browser.get_webelements(f'css:{Elements.NEWS_LIST.value}')

            for news in news_list:
                article_id = str(uuid4())
                news_title = self.browser.get_webelement(f'css:{Elements.NEWS_TITLE.value}', news)

                news_clickable = news.find_element(By.CSS_SELECTOR, Elements.LINK.value)
                news_url: str = news_clickable.get_attribute('href')
                news_url_splitted = news_url.split('-')
                news_date = '-'.join(news_url_splitted[-3:]).removesuffix('/')

                image_element = news.find_element(By.CSS_SELECTOR, Elements.IMAGE.value)
                image_url = image_element.get_attribute('src')
                image_file = self.image_path / article_id
                image_file = image_file.with_suffix('.png')
                
                self.http.download(image_url, image_file)

                article = NewsArticle(
                    article_id=article_id,
                    title=news_title,
                    date=news_date,
                    url=news_url,
                    image_path=image_file


                )


                # TODO: needs check if exists
                # if not(news_section:=news.find_element(By.CSS_SELECTOR, Elements.NEWS_SECTION.value)):
                    

                # news_section = self.browser.get_webelement(f'css:{Elements.NEWS_SECTION.value}', news)

                







        # self.browser.

        

