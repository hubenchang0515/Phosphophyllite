from jinja2 import Environment, FileSystemLoader
from .File import File

class Renderer(object):
    __env = Environment(loader=FileSystemLoader('templates'))
    
    def __init__(self, template:str) -> None:
        self.__template = Renderer.__env.get_template(template)

    def load(self, template:str) -> None:
        self.__template = Renderer.__env.get_template(template)

    def render(self, target:str, **kwargs: any) -> None:
        file = File(target)
        with file.open("w") as fp: 
            fp.write(self.__template.render(kwargs))