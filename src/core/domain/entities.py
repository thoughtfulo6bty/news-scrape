from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class NewsArticle:
    title: str
    date: datetime
    description: Optional[str] = field(init=False)
    image_filename: str
    count_phrases: Optional[int] = field(init=False)
    contains_money: Optional[bool] = field(init=False)