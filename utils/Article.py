import mistune
import subprocess
from datetime import datetime, timezone
from .MarkdownRenderer import MarkdownRenderer
from .File import File

class Article(object):
    def init(domain:str, base:str):
        Article.__markdown = mistune.create_markdown(renderer=MarkdownRenderer(domain, base), plugins=['strikethrough', 'footnotes', 'table', 'url', 'task_lists', 'def_list', 'abbr', 'mark', 'insert', 'superscript', 'subscript', 'math'])
    
    def __init__(self, path:str) -> None:
        self.__file = File(path)
        try:
            output = subprocess.run(f"git log --reverse --format=\"%ai\" -- \"{path}\"", encoding='utf-8', capture_output=True, text=True).stdout.strip()
            self.__first = datetime.strptime(output, "%Y-%m-%d %H:%M:%S %z")
        except Exception as e:
            self.__first = datetime.now(timezone.utc)

        try:
            output = subprocess.run(f"git log --format=\"%ai\" -- \"{path}\"", encoding='utf-8', capture_output=True, text=True).stdout.strip()
            self.__last = datetime.strptime(output, "%Y-%m-%d %H:%M:%S %z")
        except:
            self.__last = datetime.now(timezone.utc)


    def name(self) -> str:
        return self.__file.basename()
    
    def category(self) -> str:
        dir = File(self.__file.dirpath())
        return dir.filename()
    
    def path(self) -> str:
        return self.__file.path()
    
    def createTime(self) -> datetime:
            return self.__first
    
    def updateTime(self) -> datetime:
            return self.__last
    
    def author(self) -> str:
        return None
        
    def content(self) -> str:
        with self.__file.open() as fp:
            return Article.__markdown(fp.read())
        
    def urlPath(self) -> str:
        return f"{self.category()}/{self.name()}"
    