from .Article import Article

class Category(object):
    def __init__(self, name:str):
        self.__name = name
        self.__articles:list[str] = []
        self.__urlPath = name

    def append(self, path:str):
        self.__articles.append(path)

    def name(self) -> str:
        return self.__name

    def count(self) -> int:
        return len(self.__articles)

    def urlPath(self) -> str:
        return self.__urlPath
    
    def setUrlPath(self, urlPath: str):
        self.__urlPath = urlPath