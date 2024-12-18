from .File import File
from .Category import Category
from .Article import Article

class Scanner(object):
    def __init__(self, path:str) -> None:
        self.scan(path)

    def scan(self, path:str):
        self.__root = File(path)
        self.__categories:list[Category] = []
        self.__articles:list[Article] = []

        for catename in self.__root.listdir():
            catedir = self.__root.join(catename)
            if not catedir.isdir():
                continue

            category = Category(catename)
            print(f"{catename}:")

            for mdname in catedir.listdir():
                mdfile = catedir.join(mdname)
                if mdfile.isdir():
                    continue

                article = Article(mdfile.path())
                self.__articles.append(article)
                category.append(article)
                print(f"\t{article.name()}")

            category.sort()
            self.__categories.append(category)

        self.__articles.sort(key=lambda v: v.updateTime(), reverse=True)
        self.__categories.sort(key=lambda v: v.count(), reverse=True)

    def categories(self) -> list[Category]:
        return self.__categories
    
    def articles(self) -> list[Article]:
        return self.__articles