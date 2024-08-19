from core.domain.interfaces import Respository
from pandas import DataFrame
from robocorp.tasks import get_output_dir
from RPA.Excel.Files import Files
from pathlib import Path


class ExcelRepository(Respository):
    def __init__(self) -> None:
        self.output_dir = get_output_dir()
        self.output_path: Path = self.output_dir / 'file.csv'
        self.excel = Files()
    
    def save(self, news_articles):
        wb = self.excel.create_workbook()
        wb.create_worksheet('Results')
        self.excel.append_rows_to_worksheet(news_articles, header=True, name='Results')
        wb.save(self.output_path)