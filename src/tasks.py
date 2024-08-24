import logging
from os import getenv
from robocorp.tasks import task, get_output_dir
from core.application.scrape_news import ScrapeNews

from core.domain.interfaces import Scraper, Respository


logging.basicConfig(filename=f'{get_output_dir()}/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_scraper() -> Scraper:
    scraper_type = getenv('SCRAPER_TYPE', 'selenium')
    if scraper_type == 'selenium':
        from adapters.scraping.selenium_scraper import SeleniumScraper
        return SeleniumScraper()
    else:
        raise NotImplementedError(f'{scraper_type} not implemented yet.')

def get_repository() -> Respository:
    repository_type = getenv('REPOSITORY_TYPE', 'excel')
    if repository_type == 'excel':
        from adapters.persistence.excel_repository import ExcelRepository
        return ExcelRepository()
    else:
        raise NotImplementedError(f'{repository_type} not implemented yet.')

@task
def robot_scrape_news():
    scraper = get_scraper()
    repository = get_repository()
    scrape_app = ScrapeNews(scraper=scraper, repositoy=repository)
    scrape_app.scrape_and_save('gemini', 2)


    