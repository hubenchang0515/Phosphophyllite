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

        cateId = 1
        for catename in self.__root.listdir():
            catedir = self.__root.join(catename)
            if not catedir.isdir():
                continue

            category = Category(catename)
            category.setUrlPath(f"C{cateId}")
            print(f"{catename}:")

            mdId = 1
            for mdname in catedir.listdir():
                mdfile = catedir.join(mdname)
                if mdfile.isdir():
                    continue

                category.append(mdfile.path())
                article = Article(mdfile.path())
                article.setUrlPath(f"C{cateId}/A{mdId}")
                self.__articles.append(article)
                print(f"\t{article.name()}")
                mdId = mdId + 1

            self.__categories.append(category)
            cateId = cateId + 1

        
        self.__articles.sort(key=lambda v: v.updateTime(), reverse=True)

    def categories(self) -> list[Category]:
        return self.__categories
    
    def articles(self) -> list[Article]:
        return self.__articles