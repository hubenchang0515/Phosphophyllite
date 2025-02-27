import mistune
import subprocess
import re
from urllib.parse import quote
from datetime import datetime, timezone
from .MarkdownRenderer import MarkdownRenderer
from .File import File

class Article(object):
    def init(domain:str, base:str):
        Article.__markdown = mistune.create_markdown(renderer=MarkdownRenderer(domain, base), plugins=['strikethrough', 'footnotes', 'table', 'url', 'task_lists', 'def_list', 'abbr', 'mark', 'insert', 'superscript', 'subscript', 'math'])
    
    def __init__(self, path:str) -> None:
        self.__file = File(path)
        try:
            times = subprocess.run(["git", "log", "--reverse", "--format=%ai", path], encoding='utf-8', capture_output=True, text=True).stdout.splitlines()
            self.__first = datetime.strptime(times[0].strip(), "%Y-%m-%d %H:%M:%S %z")
            self.__last = datetime.strptime(times[-1].strip(), "%Y-%m-%d %H:%M:%S %z")
        except:
            self.__first = datetime.now(timezone.utc)
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
    
    def raw(self) -> str:
          with self.__file.open() as fp:
            return fp.read()
        
    def content(self) -> str:
        with self.__file.open() as fp:
            return Article.__markdown(fp.read())
        
    def text(self) -> str:
        text:str = re.sub(r'<[^>]*>', ' ', self.content())
        text = re.sub(r'\s+', ' ', text)
        return text
        
    def targetPath(self) -> str:
         return f"{self.category()}/{self.name()}"
        
    def urlPath(self) -> str:
        return quote(f"{self.category()}/{self.name()}")
    