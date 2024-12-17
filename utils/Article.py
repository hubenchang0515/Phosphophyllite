import mistune
from datetime import datetime, timezone
import git
from .File import File

class Article(object):
    __repo = git.Repo('.')
    __markdown = mistune.create_markdown(renderer=mistune.HTMLRenderer(), plugins=['strikethrough', 'footnotes', 'table', 'url', 'task_lists', 'def_list', 'abbr', 'mark', 'insert', 'superscript', 'subscript', 'math'])
    
    def __init__(self, path:str) -> None:
        self.__file = File(path)
        self.__first = None
        self.__last = None

        try:
            commits = Article.__repo.iter_commits(all=True, paths=[path])
            self.__first = next(commits)
            self.__last = self.__first
            for commit in commits:
                self.__last = commit
        except Exception as e:
            pass

    def name(self) -> str:
        return self.__file.basename()
    
    def category(self) -> str:
        dir = File(self.__file.dirpath())
        return dir.filename()
    
    def path(self) -> str:
        return self.__file.path()
    
    def createTime(self) -> datetime:
        if self.__last is None:
            return datetime.now(timezone.utc)
        else:
            return self.__last.committed_datetime
    
    def updateTime(self) -> datetime:
        if self.__first is None:
            return datetime.now(timezone.utc)
        else:
            return self.__first.committed_datetime
    
    def author(self) -> str:
        if self.__last is None:
            return None
        else:
            return self.__last.author
        
    def content(self) -> str:
        with self.__file.open() as fp:
            return Article.__markdown(fp.read())
        
    def urlPath(self) -> str:
        return self.__urlPath
    
    def setUrlPath(self, urlPath: str):
        self.__urlPath = urlPath