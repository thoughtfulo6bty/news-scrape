import re
from core.domain.entities import NewsArticle

class NewsProcessor:
    def __count_phrases(self, title: str, description: str) -> int:
        count_phrases = title.count('search phrase') + description.count('search phrase')
        return count_phrases
    
    def __contains_money(self, title: str, description: str | None)?
        contains_money = bool(re.search(r'\$\d+|\d+\sUSD|\d+\sdollars', title + description))
        return contains_money
    
    def process():
        ...
