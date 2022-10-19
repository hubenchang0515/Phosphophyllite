from typing import Any, Optional, List, Set, Dict
from marshmallow import Schema, fields, post_load
from datetime import datetime
from bs4 import BeautifulSoup
from utils import split_words
from urllib.parse import urlparse, ParseResult

class WebPageSchema(Schema):
    url = fields.Url()
    update_time = fields.DateTime()
    title = fields.String()
    content = fields.String()
    like = fields.Integer()
    hate = fields.Integer()
    matched_keywords = fields.List(fields.String())

    @post_load
    def make_web_page(self, data, **kwargs):
        return WebPage(**data)

class WebPage(object):
    def __init__(self, url:str="", update_time:datetime=None, title:str="", content:str="", like:int=0, hate:int=0, matched_keywords:List[str]=None) -> None:
        self.url:str = url
        self.update_time:datetime = update_time or datetime.now()
        self.title:str = title
        self.content:str = content
        self.like:int = like
        self.hate:int = hate
        self.matched_keywords:List[str] = matched_keywords or []
 
    def dump(self, only:List[str]=None, exclude:List[str]=[]) -> Dict[str, Any]:
        page_schema = WebPageSchema(only=only, exclude=exclude)
        return page_schema.dump(self)

    def dumps(self, only:List[str]=None, exclude:List[str]=[]) -> str:
        page_schema = WebPageSchema(only=only, exclude=exclude)
        return page_schema.dumps(self)

    def load(self, data:Dict[str, Any]) -> None:
        page_schema = WebPageSchema()
        page = page_schema.load(data)
        self.url = page.url
        self.update_time = page.update_time
        self.title = page.title
        self.content = page.content
        self.like = page.like
        self.hate = page.hate

    def loads(self, data:str) -> None:
        page_schema = WebPageSchema()
        page = page_schema.loads(data)
        self.url = page.url
        self.update_time = page.update_time
        self.title = page.title
        self.content = page.content
        self.like = page.like
        self.hate = page.hate

class SearchResultPageSchema(Schema):
    query = fields.String()
    page = fields.Integer()
    page_size = fields.Integer()
    page_count = fields.Integer()
    web_page_list = fields.Nested(WebPageSchema, many=True)

    @post_load
    def make_search_result_page(self, data, **kwargs):
        return SearchResultPage(**data)

class SearchResultPage(object):
    def __init__(self, query:str, page:int, page_size:int, page_count:int, web_page_list:List[WebPage]) -> None:
        self.query:str = query
        self.page:int = page
        self.page_size:int = page_size
        self.page_count:int = page_count
        self.web_page_list:List[WebPage] = web_page_list

    def dump(self, only:List[str]=None, exclude:List[str]=[]) -> Dict[str, Any]:
        schema = SearchResultPageSchema(only=only, exclude=exclude)
        return schema.dump(self)

    def dumps(self, only:List[str]=None, exclude:List[str]=[]) -> str:
        schema = SearchResultPageSchema(only=only, exclude=exclude)
        return schema.dumps(self)
        

if __name__ == "__main__":
    web_page_list:List[WebPage] = []
    web_page_list.append(WebPage(url="http://url.org", content="<html><head></head><body><title>标题</title></body></html>"))
    search_result_page = SearchResultPage("query", 0, 20, 1, web_page_list)
    print(search_result_page.dumps())
