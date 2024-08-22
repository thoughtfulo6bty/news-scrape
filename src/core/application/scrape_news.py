from core.domain.interfaces import Scraper
from datetime import datetime, date
from typing import List


class ScrapeNews:
    def __init__(self, scraper: Scraper) -> None:
        self.scraper = scraper
    
    
    def previous_months(self, opt: int) -> List[date]:
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
        return dates[::-1]
    
    def scrape(self):
        ...