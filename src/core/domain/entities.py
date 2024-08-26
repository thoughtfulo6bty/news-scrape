from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class NewsArticle:
    article_id: str
    title: str
    date: date
    url: str
    image_path: str
    selected_section: str
    extracted_section: Optional[str] = field(default_factory=str)
    description: Optional[str] = field(default_factory=str)
    count_phrases: Optional[int] = field(default_factory=int)
    contains_money: Optional[bool] = field(default_factory=bool)
