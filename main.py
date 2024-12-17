from utils import *
from config import CONFIG

PREFIX = f"build/{CONFIG['Base']}"
DES_DIR = File(PREFIX)
DES_DIR.remove()

ARTICLE_DIR = File("./blog/article")
CATEGORIES = ARTICLE_DIR.listdir()

staticDir = File("static")
staticDir.copyTo(f"{PREFIX}/static")

scanner = Scanner(ARTICLE_DIR.path())

def renderIndex():
    DATA = {
        "Domain": CONFIG["Domain"],
        "Base": CONFIG["Base"],
        "Title": CONFIG['Title'],
        "Nickname": CONFIG["Nickname"],
        "Username": CONFIG["Username"],
        "Avatar": f"https://github.com/{CONFIG['Username']}.png",
        "Categories": scanner.categories(),
        "Articles": scanner.articles(),
        "Article": scanner.articles()[0] if len(scanner.articles()) > 0 else None,
    }

    renderer = Renderer("index.html")
    renderer.render(f"{PREFIX}/index.html", DATA=DATA)

def renderArticle(article:Article):
    DATA = {
        "Domain": CONFIG["Domain"],
        "Base": CONFIG["Base"],
        "Title": CONFIG['Title'],
        "Nickname": CONFIG["Nickname"],
        "Username": CONFIG["Username"],
        "Avatar": f"https://github.com/{CONFIG['Username']}.png",
        "Categories": scanner.categories(),
        "Articles": scanner.articles(),
        "Article": article,
    }

    renderer = Renderer("index.html")
    renderer.render(f"{PREFIX}/articles/{article.urlPath()}.html", DATA=DATA)

def renderSitemap():
    DATA = {
        "Domain": CONFIG["Domain"],
        "Base": CONFIG["Base"],
        "Articles": scanner.articles(),
    }
    renderer = Renderer("sitemap.txt")
    renderer.render(f"{PREFIX}/sitemap.txt", DATA=DATA)


if __name__ == "__main__":

    for article in scanner.articles():
        renderArticle(article)

    renderIndex()
    renderSitemap()