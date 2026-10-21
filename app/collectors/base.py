from abc import ABC, abstractmethod
from app.schemas import NewsItem
class NewsCollector(ABC):
    name = "base"
    @abstractmethod
    def fetch(self) -> list[NewsItem]: ...
