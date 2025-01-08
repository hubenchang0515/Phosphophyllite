import math
import subprocess
from utils import *
from config import CONFIG

CURRENT_FILE = File(__file__)
CURRENT_DIR = File(CURRENT_FILE.dirpath())
TARGET_DIR = CURRENT_DIR.join("build", CONFIG['Base'])
PREFIX = TARGET_DIR.path()

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
        renderer.render(f"{PREFIX}/categories/{category.targetPath()}-{page+1}.html", DATA=DATA)

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
    renderer.render(f"{PREFIX}/articles/{article.targetPath()}.html", DATA=DATA)

def renderSitemap(articles:list[Article]):
    sites:list[str] = []
    for article in articles:
        sites.append(f"https://{CONFIG['Username']}.github.io/{CONFIG['Base']}/articles/{article.urlPath()}.html")
    DATA = {
        "Sites": sites,
    }
    renderer = Renderer("sitemap.txt")
    renderer.render(f"{PREFIX}/sitemap.txt", DATA=DATA)

def deploy(target:str):
    origin = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "init", "."], cwd=target)
    subprocess.run(["git", "remote", "add", "origin", origin], cwd=target)
    subprocess.run(["git", "checkout", "-b", "gh-pages"], cwd=target)
    subprocess.run(["git", "add", "*"], cwd=target)
    subprocess.run(["git", "commit", "-m", "\"Update gh-pages\""], cwd=target)
    subprocess.run(["git", "push", "-f", "origin", "gh-pages"], cwd=target)

if __name__ == "__main__":
    Article.init(f"https://{CONFIG['Username']}.github.io", CONFIG['Base'])
    try:
        TARGET_DIR.remove()
    except:
        print("删除失败，没有权限，请手动删除 build 目录")

    ARTICLE_DIR = CURRENT_DIR.join("blog", "article")
    CATEGORIES = ARTICLE_DIR.listdir()

    STATIC_DIR = CURRENT_DIR.join("static")
    STATIC_DIR.copyTo(f"{PREFIX}/static")

    RESOURCE_DIR = CURRENT_DIR.join("blog", "resource")
    RESOURCE_DIR.copyTo(f"{PREFIX}/resource")

    scanner = Scanner(ARTICLE_DIR.path())
    articles = scanner.articles()
    categories = scanner.categories()

    for article in scanner.articles():
        renderArticle(article, articles, categories)

    for category in scanner.categories():
        renderCategory(category, articles, categories, 10)

    renderIndex(articles, categories)
    renderSitemap(articles)

    deploy(TARGET_DIR.path())