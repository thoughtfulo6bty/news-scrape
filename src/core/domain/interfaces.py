from abc import ABC, abstractmethod
from typing import Optional, List, Literal
from datetime import date
from core.domain.entities import NewsArticle


class Scraper(ABC):
    @abstractmethod
    def scrape_news(self, scrape_id: str, search_phrase: str, earliest_date: date, 
                    section: Literal['all', 'world', 'business', 'legal', 
                                     'markets', 'breakingviews', 'technology', 
                                     'sustainability', 'science', 'sports', 'lifestyle']) -> Optional[List[NewsArticle]]:
        raise NotImplementedError('Scrape News Not Implemented Yet.')
    

class Respository(ABC):
    @abstractmethod
    def save(self, scrape_id: str, news_articles: List[NewsArticle]):
        pass