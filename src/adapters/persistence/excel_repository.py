from core.domain.interfaces import Respository
from robocorp.tasks import get_output_dir
from pathlib import Path
from pandas import DataFrame
from typing import List
from core.domain.entities import NewsArticle
from dataclasses import asdict
import logging


class ExcelRepository(Respository):
    def __init__(self) -> None:
        self.output_dir = get_output_dir()


    def save(self, scrape_id: str, news_list: List[NewsArticle]):
        filename = Path(f'news_scrape_result_{scrape_id}').with_suffix('.xlsx')
        output_path: Path = self.output_dir / f'results_{scrape_id}' / filename

        news_list_dict = list(map(asdict, news_list))
        df = DataFrame(news_list_dict)
        df.to_excel(output_path, 
                    sheet_name=f'results_{scrape_id}', 
                    index=False)
        logging.info(f'Results Saved in: {output_path}')
        