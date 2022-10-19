#! /usr/bin/env python3

from typing import Any, Optional, List, Set, Dict
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import load_only
from functools import reduce
import math

from utils import split_words
from schema import WebPage, SearchResultPage
from model import DBSession, WebPageModel, InvertedIndexModel

class PageInfo(object):
    def __init__(self, page_id:int) -> None:
        self.page_id:int = page_id
        self.keyword_scores:Dict[str,  float] = {}

    def scores(self) -> int:
        return reduce(lambda x,y:x+y, self.keyword_scores.values())

class SearchResult(object):
    def __init__(self, query:str) -> None:
        self.__query:str = query
        self.__page_infos:Dict[str, PageInfo] = {}

    def infos(self) -> Dict[str, PageInfo]:
        return self.__page_infos

    def update(self, keyword:str, web_page_id_scores:Dict[int, float], web_page_count:int) -> None:
        # TF-IDF
        idf:float = math.log(web_page_count / len(web_page_id_scores) + 1)
        for web_page_id in web_page_id_scores:
            if web_page_id not in self.__page_infos:
                self.__page_infos[web_page_id] = PageInfo(web_page_id)
            self.__page_infos[web_page_id].keyword_scores[keyword] = web_page_id_scores[web_page_id] * idf

    def get_webpages(self, page:int=0, page_size:int=20) -> List[WebPage]:
        page_infos:List[PageInfo] = list(self.__page_infos.values())
        page_infos.sort(key=lambda x:x.scores(), reverse=True)
        page_infos = page_infos[page*page_size:(page+1)*page_size]
        webpages:List[WebPage] = []
        session = DBSession()
        for page_info in page_infos:
            page_model = session.query(WebPageModel).filter_by(id=page_info.page_id).first()
            if page_model is None:
                continue
            webpages.append(WebPage(url=page_model.url, 
                                    update_time=page_model.update_time, 
                                    title=page_model.title, 
                                    content=page_model.content,
                                    like=page_model.like,
                                    matched_keywords=page_info.keyword_scores.keys()))
        return webpages

    def total(self) -> int:
        return len(self.__page_infos)

    def dump(self, page:int=0, page_size:int=20, only:Optional[Set[str]]=None, exclude:Optional[Set[str]]=None) -> List[Dict[str, Any]]:
        web_page_list:List[WebPage] = self.get_webpages(page=page, page_size=page_size)
        search_result_page = SearchResultPage(query=self.__query,
                                                page=page, 
                                                page_size=page_size, 
                                                page_count=self.total() / page_size, 
                                                web_page_list=web_page_list)
        return search_result_page.dump()

    def dumps(self, page:int=0, page_size:int=20, only:Optional[Set[str]]=None, exclude:Optional[Set[str]]=None) -> str:
        web_page_list:List[WebPage] = self.get_webpages(page=page, page_size=page_size)
        search_result_page = SearchResultPage(query=self.__query,
                                                page=page, 
                                                page_size=page_size, 
                                                page_count=self.total() / page_size, 
                                                web_page_list=web_page_list)
        return search_result_page.dumps()



class Searcher(object):
    def __init__(self) -> None:
        pass

    def keywords(self, text:str) -> List[str]:
        return split_words(text)

    def search(self, text:str) -> SearchResult:
        cols:List[str] = ["url", "update_time", "title", "like", "hate"]
        search_result = SearchResult(query=text)
        session = DBSession()
        web_page_count:int = session.query(func.count(WebPageModel.id)).scalar()
        keywords:List[str] = self.keywords(text)
        index_models = session.query(InvertedIndexModel).filter(InvertedIndexModel.keyword.in_(keywords))
        if index_models is None:
            return search_result
        for index_model in index_models:
            web_page_id_scores:Dict[int, float] = eval(f"{index_model.web_page_id_scores}")
            search_result.update(index_model.keyword, web_page_id_scores, web_page_count)
        return search_result

if __name__ == "__main__":
    import sys
    searcher = Searcher()
    result = searcher.search(sys.argv[1])
    print(result.dumps())
