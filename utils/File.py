import os
import shutil

class File(object):
    def __init__(self, path:str) -> None:
        self.__path = os.path.abspath(path)

    def path(self) -> str:
        return self.__path
    
    def filename(self) -> str:
        return os.path.basename(self.__path)
    
    def basename(self) -> str:
        return os.path.splitext(self.filename())[0]
    
    def dirpath(self) -> str:
        return os.path.dirname(self.__path)
    
    def join(self, *subs:str) -> 'File':
        return File(os.path.join(self.__path, *subs))
    
    def listdir(self,key:None=None) -> list[str]:
        files:list[str] = os.listdir(self.__path)
        files.sort(key=key)
        return files
    
    def exists(self) -> bool:
        return os.path.exists(self.__path)
    
    def isdir(self) -> bool:
        return os.path.isdir(self.__path)

    def remove(self) -> None:
        if not self.exists():
            return
        elif not self.isdir():
            os.remove(self.__path)
        else:
            for filename in self.listdir():
                self.join(filename).remove()
            os.rmdir(self.__path)
    
    def open(self, mode:str="r") -> any:
        if not os.path.exists(self.dirpath()):
            os.makedirs(self.dirpath())

        return open(self.__path, mode, encoding="utf-8")
    
    def copyTo(self, target:str) -> any:
        shutil.copytree(self.path(), target, dirs_exist_ok=True)

    def mtime(self) -> float:
        return os.path.getmtime(self.__path)
    
    def ctime(self) -> float:
        return os.path.getctime(self.__path)