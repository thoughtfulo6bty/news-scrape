from core.domain.interfaces import Scraper
from core.domain.news_processor import contains_money, count_phrases
from datetime import datetime, date
from typing import Tuple


class ScrapeNews:
    def __init__(self, scraper: Scraper) -> None:
        self.scraper = scraper
    
    
    def get_search_months(self, opt: int) -> Tuple[date, date]:
        if opt < 0:
            raise ValueError("The number of months must be non-negative.")
        today: date = datetime.date.today().replace(day=1)
        dates = [today]
        for _ in range(opt - 1):
            if today.month == 1:
                today = today.replace(year=today.year - 1, month=12)
            else:
                today = today.replace(month=today.month - 1)
            dates.append(today)
        dates = dates[::-1]
        return dates[0], dates[-1]
    
    
    def scrape(self, search_phrase: str, date_option: int, section: str = None):
        previous_date, _ = self.get_search_months(date_option)
        
        news_list = self.scraper.scrape_news(
            search_phrase=search_phrase,
            previous_date=previous_date,
            section=section
        )

        for article in news_list:
            article.contains_money = contains_money(title=article.title,
                                                    description=article.description)
            article.count_phrases = count_phrases(title=article.title,
                                                    description=article.description)
