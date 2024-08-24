from core.domain.interfaces import Scraper
from core.domain.interfaces import Respository
from core.domain.news_processor import contains_money, count_phrases
from datetime import date
from typing import Tuple
from uuid import uuid4
import logging


class ScrapeNews:
    def __init__(self, scraper: Scraper, repositoy: Respository):
        self.scraper = scraper
        self.repository = repositoy
        self._scrape_id = None


    @property
    def scrape_id(self) -> str:
        """
        Generates and returns a unique scrape ID if it has not already been set.

        The scrape ID is a string derived from the first segment of a newly generated UUID.
        If the scrape ID has already been set (i.e., is not `None`), it simply returns the
        existing ID.

        Returns:
            str: A unique scrape ID.
        """
        if self._scrape_id is None:
            self._scrape_id = str(uuid4()).split('-')[0]
        return self._scrape_id

    
    def get_search_months(self, opt: int) -> Tuple[date, date]:
        """
        Returns a tuple of two dates representing the first day of the earliest month 
        and the first day of the latest month based on the specified number of months.

        The function calculates the start date of the first month and the last month in the range
        of the given number of months. The `opt` parameter specifies how many months back from 
        the current month should be considered. For example, if `opt` is 3 and the current month 
        is August, it will return the first day of June and the first day of August.

        Args:
            opt (int): The number of months to include in the search range. Must be non-negative.

        Returns:
            Tuple[date, date]: A tuple containing two dates:
                - The first date is the first day of the earliest month in the range.
                - The second date is the first day of the latest month in the range.
                
        Raises:
            ValueError: If `opt` is negative.
        """
        if opt < 0:
            raise ValueError("The number of months must be non-negative.")
        today: date = date.today().replace(day=1)
        dates = [today]
        for _ in range(opt - 1):
            if today.month == 1:
                today = today.replace(year=today.year - 1, month=12)
            else:
                today = today.replace(month=today.month - 1)
            dates.append(today)
        dates = dates[::-1]
        return dates[0], dates[-1]
    

    def scrape_and_save(self, search_phrase: str, date_option: int, section: str = 'all'):
        earliest_date, _ = self.get_search_months(date_option)
        
        logging.info(f'Scrape ID: {self.scrape_id}')

        news_list = self.scraper.scrape_news(
            scrape_id=self.scrape_id,
            search_phrase=search_phrase,
            earliest_date=earliest_date,
            section=section
        )

        

        # TODO: implements flow if not exists news
        for article in news_list:
            article.contains_money = contains_money(title=article.title,
                                                    description=article.description)
            article.count_phrases = count_phrases(title=article.title,
                                                    description=article.description)
        
        self.repository.save(news_list)


    