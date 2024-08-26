from abc import ABC, abstractmethod
from datetime import date
from typing import List, Literal, Optional
from core.domain.entities import NewsArticle


class Scraper(ABC):
    """
    Abstract base class for defining a news scraper.

    Methods:
        scrape_news(scrape_id: str,
                    search_phrase: str,
                    earliest_date: date,
                    section: Literal) -> Optional[List[NewsArticle]]:
            Abstract method to scrape news articles based on the provided search criteria.
    """

    @abstractmethod
    def scrape_news(
        self,
        scrape_id: str,
        search_phrase: str,
        earliest_date: date,
        section: Literal[
            "all",
            "world",
            "business",
            "legal",
            "markets",
            "breakingviews",
            "technology",
            "sustainability",
            "science",
            "sports",
            "lifestyle",
        ],
    ) -> Optional[List[NewsArticle]]:
        """
        Scrapes news articles based on the provided search criteria.

        Args:
            scrape_id (str): The unique identifier for the scrape operation.
            search_phrase (str): The phrase to search for in news articles.
            earliest_date (date): The earliest publication date for the articles.
            section (Literal): The news section to filter by, with specific allowable values.

        Returns:
            Optional[List[NewsArticle]]: A list of NewsArticle objects if articles are found, otherwise None.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Scrape News Not Implemented Yet.")


class Respository(ABC):
    """
    Abstract base class for defining a repository to save news articles.

    Methods:
        save(scrape_id: str, news_list: List[NewsArticle]) -> None:
            Abstract method to save a list of news articles.
    """

    @abstractmethod
    def save(self, scrape_id: str, news_list: List[NewsArticle]):
        """
        Saves the list of news articles.

        Args:
            scrape_id (str): The unique identifier for the scrape operation.
            news_list (List[NewsArticle]): A list of news articles to save.

        Returns:
            None
        """
        raise NotImplementedError("Save Not Implemented Yet.")
