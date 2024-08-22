from abc import ABC, abstractmethod
from typing import Optional, List
from core.domain.entities import NewsArticle


class Scraper(ABC):
    @abstractmethod
    def scrape_news(self, search_phrase, previous_date, section) -> Optional[List[NewsArticle]]:
        raise NotImplementedError('Scrape News Not Implemented Yet.')
    

class Respository(ABC):
    @abstractmethod
    def save(self, news_articles):
        pass