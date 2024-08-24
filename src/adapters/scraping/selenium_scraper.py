import logging
from enum import Enum
from typing import List, Optional
from uuid import uuid4
from datetime import date, datetime

from robocorp.tasks import get_output_dir
from RPA.Browser.Selenium import Selenium
from RPA.Browser.Selenium import ElementNotFound
from RPA.HTTP import HTTP
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from datetime import timedelta

import undetected_chromedriver as uc

from core.domain.entities import NewsArticle
from core.domain.interfaces import Scraper




class Elements(Enum):
    SEARCH_TITLE = '//*[@id="main-content"]'
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
        self._driver = None

        
        # TODO: using another lib, like requests or urllib, because HTTP RPA slow download image
        # self.http = HTTP()
    
    @property
    def driver(self):
        if self._driver is None:
            chrome_options = Options()
            chrome_options.page_load_strategy = 'eager' 
            self._driver = uc.Chrome(options=chrome_options)
        return self._driver 


    def scrape_news(self, scrape_id: str, search_phrase: str,
                    earliest_date: date,
                    section: str = 'all') -> Optional[List[NewsArticle]]:
        
        logging.info(f'Search Phrase: {search_phrase}')
        logging.info(f'Section: {section}')


        query =  '+'.join(search_phrase.split())
        offset = self.offset.format(0)

        url = self.base_url.format(query, section, offset)

        # exploring captcha breaker
        browser_alias = 'undetected_chrome'
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
                    (By.XPATH, Elements.ALL_OFFSET.value.removeprefix('xpath:'))
                )
            )
        except TimeoutException:
            logging.error(f'No search result match the term: {search_phrase}')
            logging.warning(self.browser.get_source())
            self.browser.close_browser()
            return
        
        max_offset = int(offset_element.text.split()[-1])
        offsets = range(0, max_offset, 20)

        logging.info(f'Offset range: {max_offset//20}')

        news_articles = []
        break_scrape = False

        for offset in offsets:
            # exploring wait from RPAframework
            try:
                self.browser.wait_until_page_contains_element(f'xpath:{Elements.SEARCH_TITLE.value}', 40)
            except TimeoutException:
                logging.error('Lazy page.')
                return

            news_list = self.browser.get_webelements(f'css:{Elements.NEWS_LIST.value}')
            total_height: int = self.browser.execute_javascript("return document.body.scrollHeight")
            scroll_height = (total_height*0.8)//len(news_list)
            scroll_coord = 0

            for news in news_list:
                scroll_coord += scroll_height
                article_id = str(uuid4())
                self.browser.execute_javascript(f"window.scrollBy(0, {scroll_coord});")
                news_title = self.browser.get_webelement(f'css:{Elements.NEWS_TITLE.value}', news)
                logging.info(f'Collecting: {news_title.text}')

                news_clickable = news.find_element(By.CSS_SELECTOR, Elements.LINK.value)
                news_url: str = news_clickable.get_attribute('href')
                news_url_splitted = news_url.split('-')
                news_date = '-'.join(news_url_splitted[-3:]).removesuffix('/')
                news_date = datetime.strptime(news_date, "%Y-%m-%d").date()

                if news_date < earliest_date:
                    break_scrape = True
                    break
                
                try:
                    article_section = self.browser.get_webelement(f'css:{Elements.NEWS_SECTION.value}', news).text
                except ElementNotFound:
                    article_section = None


                logging.info(f'Saving thumbnail: {news_title}')

                self.image_path = get_output_dir() / f'results_{scrape_id}' / 'thumbnails'
                self.image_path.mkdir(exist_ok=True, parents=True)

                image_element = news.find_element(By.CSS_SELECTOR, Elements.IMAGE.value)
                image_url = image_element.get_attribute('src')
                image_file = self.image_path / article_id
                image_file = image_file.with_suffix('.png')
                
                # self.http.download(image_url, image_file)


                article = NewsArticle(
                    article_id=article_id,
                    title=news_title.text,
                    date=news_date,
                    url=news_url,
                    image_path=str(image_file),
                    extracted_section=article_section,
                    selected_section=section
                )
                                
                news_articles.append(article)
            
            if not break_scrape:
                self.browser.execute_javascript("window.stop();")
                logging.info(f'Go to Offset: {offset}')
                self.browser.go_to(self.base_url.format(query, section, offset))
            else:
                logging.info(f'Finish Scrape in offset: {offset}')
        
        self.browser.close_all_browsers()
        return news_articles
