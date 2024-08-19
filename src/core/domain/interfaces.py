from abc import ABC, abstractmethod


class Scraper(ABC):
    @abstractmethod
    def scrape_news(self, search_phrase, category, months):
        raise NotImplementedError('Scrape News Not Implemented Yet.')
    

class Respository(ABC):
    @abstractmethod
    def save(self, news_articles):
        pass