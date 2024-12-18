from urllib.parse import quote
from .Article import Article

class Category(object):
    def __init__(self, name:str):
        self.__name = name
        self.__articles:list[Article] = []

    def append(self, article:Article):
        self.__articles.append(article)

    def articles(self) -> list[Article]:
        return self.__articles
    
    def sort(self):
        self.__articles.sort(key=lambda v: v.updateTime(), reverse=True)

    def name(self) -> str:
        return self.__name

    def count(self) -> int:
        return len(self.__articles)

    def targetPath(self) -> str:
        return self.__name

    def urlPath(self) -> str:
        return quote(self.__name)