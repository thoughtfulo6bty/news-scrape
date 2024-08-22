from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime
from PIL.Image import Image


@dataclass
class NewsArticle:
    article_id: str
    title: str
    date: datetime
    url: str
    image_path: str
    extracted_section: Optional[str] = field(init=False)
    selected_section: Optional[str] = field(init=False)
    description: Optional[str] = field(init=False)
    count_phrases: Optional[int] = field(init=False)
    contains_money: Optional[bool] = field(init=False)