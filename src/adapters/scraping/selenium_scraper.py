import logging
from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional
from uuid import uuid4
from datetime import date, datetime

from robocorp.tasks import get_output_dir
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.domain.entities import NewsArticle
from core.domain.interfaces import Scraper

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
        self.base_url = 'https://www.reuters.com/site-search/?query={}&section={}&{}&date=any_time&sort=newest'
        self.browser = Selenium()
        self.http = HTTP()

        # TODO: remove mock
        # self.image_path = get_output_dir() / 'thumbnails'
        self.image_path = Path('thumbnails')
        self.image_path.mkdir(exist_ok=True)


    def scrape_news(self, search_phrase: str,
                    previous_date: date,
                    section: Literal['all', 'world', 'business', 'legal', 
                                     'markets', 'breakingviews', 'technology', 
                                     'sustainability', 'science', 'sports', 'lifestyle', ] = 'all') -> Optional[List[NewsArticle]]:
        
        print(f'Search Phrase: {search_phrase}')
        print(f'Section: {section}')


        query =  '+'.join(search_phrase.split())
        offset = self.offset.format(0)

        url = self.base_url.format(query, section, offset)
        self.browser.open_available_browser(url=url, maximized=True, headless=True, options={'capabilities': {"pageLoadStrategy": "eager"}})    
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

        print(f'Offset range: {max_offset//20}')

        news_articles = []
        break_scrape = False

        for offset in offsets:
            news_list = self.browser.get_webelements(f'css:{Elements.NEWS_LIST.value}')

            for news in news_list:
                article_id = str(uuid4())
                news_title = self.browser.get_webelement(f'css:{Elements.NEWS_TITLE.value}', news)
                print(f'Collecting: {news_title}')

                news_clickable = news.find_element(By.CSS_SELECTOR, Elements.LINK.value)
                news_url: str = news_clickable.get_attribute('href')
                news_url_splitted = news_url.split('-')
                news_date = '-'.join(news_url_splitted[-3:]).removesuffix('/')
                news_date = datetime.strptime(news_date, "%Y-%m-%d").date()

                if news_date < previous_date:
                    break_scrape = True
                    break
                
                try:
                    article_section = self.browser.get_webelement(f'css:{Elements.NEWS_SECTION.value}', news)
                except NoSuchElementException:
                    article_section = None


                print(f'Saving thumbnail: {news_title}')

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
                    image_path=str(image_file),
                    extracted_section=article_section,
                    selected_section=section
                )
                
                article.selected_section = section
                
                news_articles.append(article)
            
            if not break_scrape:
                self.browser.go_to(self.base_url.format(query, section, offset))
            else:
                print(f'Finish Scrape in offset: {offset}')
        
        self.browser.close_all_browsers()
