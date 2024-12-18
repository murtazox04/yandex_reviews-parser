from dataclasses import dataclass
from typing import Union


@dataclass
class Review:
    review_id: str
    likes: int
    name: str
    icon_href: Union[str, None]
    date: float
    text: str
    stars: float
    answer: str


@dataclass
class Info:
    name: str
    rating: float
    count_rating: int
    stars: float
