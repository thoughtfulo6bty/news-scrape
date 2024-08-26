import json
import logging
from os import getenv
from robocorp.tasks import get_output_dir, task
from robocorp.workitems import inputs
from core.application.scrape_news import ScrapeNews
from core.domain.interfaces import Respository, Scraper

logging.basicConfig(
    filename=f"{get_output_dir()}/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_scraper() -> Scraper:
    """
    Factory function to return an instance of a Scraper based on the SCRAPER_TYPE environment variable.

    Returns:
        Scraper: An instance of a Scraper implementation.

    Raises:
        NotImplementedError: If the SCRAPER_TYPE environment variable is set to a type that is not implemented.
    """
    scraper_type = getenv("SCRAPER_TYPE", "selenium")
    if scraper_type == "selenium":
        from adapters.scraping.selenium_scraper import SeleniumScraper

        return SeleniumScraper()
    else:
        raise NotImplementedError(f"{scraper_type} not implemented yet.")


def get_repository() -> Respository:
    """
    Factory function to return an instance of a Repository based on the REPOSITORY_TYPE environment variable.

    Returns:
        Repository: An instance of a Repository implementation.

    Raises:
        NotImplementedError: If the REPOSITORY_TYPE environment variable is set to a type that is not implemented.
    """
    repository_type = getenv("REPOSITORY_TYPE", "excel")
    if repository_type == "excel":
        from adapters.persistence.excel_repository import ExcelRepository

        return ExcelRepository()
    else:
        raise NotImplementedError(f"{repository_type} not implemented yet.")


@task
def robot_scrape_news():
    """
    Function to scrape news with parameters using robocorp decorator
    """
    #  payload = json.loads(inputs.current.payload)

    # mocked payload
    payload = {'search_phrase': 'gemini', 'date_option': 0, 'section': 'all'}

    search_phrase = payload['search_phrase'].lower()
    date_option = int(payload['date_option'])
    section = payload['section']

    if not search_phrase:
        logging.error('Search phrase not defined. Breaking scrape.')
    else:
        scraper = get_scraper()
        repository = get_repository()
        scrape_app = ScrapeNews(scraper=scraper, repositoy=repository)
        scrape_app.scrape_and_save(search_phrase, date_option, section)
