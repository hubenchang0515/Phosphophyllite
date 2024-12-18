import math
from urllib.parse import quote
from utils import *
from config import CONFIG

PREFIX = f"build/{CONFIG['Base']}"
DES_DIR = File(PREFIX)


def renderIndex(articles:list[Article], categories:list[Category]):
    DATA = {
        "Domain": f"https://{CONFIG['Username']}.github.io",
        "Base": CONFIG["Base"],
            "Title": f"{CONFIG['Nickname']} 的博客 - 首页",
        "Nickname": CONFIG["Nickname"],
        "Username": CONFIG["Username"],
        "Friends": CONFIG["Friends"],
        "Avatar": f"https://github.com/{CONFIG['Username']}.png",
        "Categories": categories,
        "Articles": articles,
        "Article": articles[0] if len(articles) > 0 else None,
    }

    renderer = Renderer("index.html")
    renderer.render(f"{PREFIX}/index.html", DATA=DATA)

def renderCategory(category:Category, articles:list[Article], categories:list[Category], pageSize:int):
    pageCount = math.ceil(len(category.articles())/pageSize)
    for page in range(0, pageCount):
        DATA = {
            "Domain": f"https://{CONFIG['Username']}.github.io",
            "Base": CONFIG["Base"],
            "Title": f"{CONFIG['Nickname']} 的博客 - {category.name()}",
            "Nickname": CONFIG["Nickname"],
            "Username": CONFIG["Username"],
            "Friends": CONFIG["Friends"],
            "Avatar": f"https://github.com/{CONFIG['Username']}.png",
            "Categories": categories,
            "Articles": articles,
            "Category": category,
            "Page": page,
            "PageSize": pageSize,
            "PageCount": pageCount,
        }

        renderer = Renderer("category.html")
        renderer.render(f"{PREFIX}/categories/{category.urlPath()}-{page+1}.html", DATA=DATA)

def renderArticle(article:Article, articles:list[Article], categories:list[Category]):
    DATA = {
        "Domain": f"https://{CONFIG['Username']}.github.io",
        "Base": CONFIG["Base"],
            "Title": f"{CONFIG['Nickname']} 的博客 - {article.name()}",
        "Nickname": CONFIG["Nickname"],
        "Username": CONFIG["Username"],
        "Friends": CONFIG["Friends"],
        "Avatar": f"https://github.com/{CONFIG['Username']}.png",
        "Categories": categories,
        "Articles": articles,
        "Article": article,
    }

    renderer = Renderer("article.html")
    renderer.render(f"{PREFIX}/articles/{article.urlPath()}.html", DATA=DATA)

def renderSitemap(articles:list[Article]):
    sites:list[str] = []
    for article in articles:
        sites.append(f"https://{CONFIG['Username']}.github.io/{CONFIG['Base']}/articles/{quote(article.urlPath())}.html")
    DATA = {
        "Sites": sites,
    }
    renderer = Renderer("sitemap.txt")
    renderer.render(f"{PREFIX}/sitemap.txt", DATA=DATA)


if __name__ == "__main__":
    DES_DIR.remove()

    ARTICLE_DIR = File("./blog/article")
    CATEGORIES = ARTICLE_DIR.listdir()

    staticDir = File("static")
    staticDir.copyTo(f"{PREFIX}/static")

    scanner = Scanner(ARTICLE_DIR.path())
    articles = scanner.articles()
    categories = scanner.categories()

    for article in scanner.articles():
        renderArticle(article, articles, categories)

    for category in scanner.categories():
        renderCategory(category, articles, categories, 10)

    renderIndex(articles, categories)
    renderSitemap(articles)