import logging
from dataclasses import asdict
from pathlib import Path
from typing import List
from pandas import DataFrame
from robocorp.tasks import get_output_dir
from core.domain.entities import NewsArticle
from core.domain.interfaces import Respository


class ExcelRepository(Respository):
    def __init__(self) -> None:
        self.output_dir = get_output_dir()

    def save(self, scrape_id: str, news_list: List[NewsArticle]):
        """
        Saves the list of news articles to an Excel file.

        Args:
            scrape_id (str): The ID of the scrape, used for naming the output file.
            news_list (List[NewsArticle]): A list of news articles to save.

        Returns:
            None
        """
        filename = Path(f"news_scrape_result_{scrape_id}").with_suffix(".xlsx")
        output_path: Path = self.output_dir / filename

        news_list_dict = list(map(asdict, news_list))
        df = DataFrame(news_list_dict)
        df.to_excel(output_path, sheet_name=f"results_{scrape_id}", index=False)
        logging.info(f"Results Saved in: {output_path}")
