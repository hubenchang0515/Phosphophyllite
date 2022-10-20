#! /usr/bin/env python3

import logging
import requests
from datetime import datetime, timedelta
from typing import Union, Optional, Set, List
from sqlalchemy.orm import load_only

import config
from analyzer import WebPageAnalyzer
from schema import WebPage
from model import DBSession, InvertedIndexModel, WebPageModel, SpiderQueueModel

logger = logging.getLogger("spider")

class SpiderQueue(object):

    def __init__(self, max:int=0) -> None:
        self.__max:int = 0

    def count(self) -> int:
        session = DBSession()
        return session.query(func.count(WebPageModel.id)).scalar()

    def empty(self) -> bool:
        return self.count() == 0

    def full(self) -> bool:
        return self.__max > 0 and self.count() == self.__max

    def pop_url(self) -> str:
        session = DBSession()
        item = session.query(SpiderQueueModel).first()
        if item is None:
            return None

        url = item.url
        session.delete(item)
        session.commit()
        return url

    def push_url(self, url:str) -> bool:
        if len(url) > config.sql_index_field_length_limit:
            logger.warning(f"{url} is too long, skip.")
            return False

        if self.full():
            return False

        session = DBSession()
        item = session.query(SpiderQueueModel).filter_by(url=url).first()
        if item is not None:
            return False
        item = SpiderQueueModel(url=url)
        session.add(item)
        session.commit()
        return True

    def push_urls(self, urls:List[str]) -> int:
        count:int = self.count()
        session = DBSession()
        for url in urls:
            if len(url) > config.sql_index_field_length_limit:
                logger.warning(f"{url} is too long, skip.")
                continue

            if count >= config.spider_queue_max_size:
                break
                
            item = session.query(SpiderQueueModel).filter_by(url=url).first()
            if item is not None:
                continue
            item = SpiderQueueModel(url=url)
            session.add(item)
            count += 1
        session.commit()
        return count


class Spider(object):

    def __init__(self) -> None:
        self.__url_queue = SpiderQueue(config.spider_queue_max_size)
        self.__proxy = config.proxy
        self.__timeout:int = config.timeout
        self.__headers:dict[str, str] = {"User-Agent": config.user_agent}

    def push_url(self, url:str) -> None:
        self.__url_queue.push_url(url)

    def pop_url(self) -> Optional[str]:
        return self.__url_queue.pop_url()

    def push_urls(self, urls:Union[Set[str], List[str]]) -> None:
        self.__url_queue.push_urls(urls)

    def update_webpage(self, web_page_analyzer:WebPageAnalyzer) -> int:
        session = DBSession()
        page_model = session.query(WebPageModel).filter_by(url=web_page_analyzer.url()).options(load_only("id")).first()
        if page_model is None:
            page_model = WebPageModel(url=web_page_analyzer.url(), 
                                        update_time=datetime.now(), 
                                        title=web_page_analyzer.title(), 
                                        content=web_page_analyzer.content())
        else:
            page_model.update_time = datetime.now()
            page_model.title = web_page_analyzer.title()
            page_model.content = web_page_analyzer.content()
        session.add(page_model)
        session.commit()
        return page_model.id

    def guess_charset(self, response:requests.Response) -> str:
        try:
            encoding:str = response.encoding.upper()
            apparent_encoding:str = response.apparent_encoding.upper()
            info:List[str] = [encoding, apparent_encoding]

            if "GB2312" in info:
                return "GB2312"

            if "GBK" in info:
                return "GBK"
        except Exception as e:
            logger.warning(e)
        
        return "UTF-8"

    def request(self, url:str) -> Optional[WebPageAnalyzer]:
        try:
            response:requests.Response = requests.get(url, 
                                                        stream=True,
                                                        proxies=self.__proxy, 
                                                        timeout=self.__timeout, 
                                                        headers=self.__headers)
        except Exception as e:
            logger.warning(e)
            return None

        if response.status_code != 200:
            logger.warning(f"{url} - status code:{response.status_code}")
            response.close()
            return None

        if "content-type" not in response.headers:
            logger.warning(f"{url} - response.headers without content-type")
            response.close()
            return None

        if "text/html" not in response.headers["content-type"]:
            logger.warning(f"{url} - content-type {response.headers['content-type']} is not text/html")
            response.close()
            return None

        response.encoding = self.guess_charset(response)
        web_page_analyzer = WebPageAnalyzer(url=url, html=response.text)
        response.close()
        return web_page_analyzer

    def expired(self, url:str, cd:timedelta) -> bool:
        session = DBSession()
        page = session.query(WebPageModel).filter_by(url=url).first()
        if page is None:
            return True
        
        if page.update_time < self.__start_time:
            return True

        return datetime.now() - page.update_time > cd

    def update_inverted_index(self, web_page_id:int, web_page_analyzer:WebPageAnalyzer) -> int:
        session = DBSession()
        scores:Dict[str, float] = web_page_analyzer.keyword_scores()
        for keyword in scores:
            index = session.query(InvertedIndexModel).filter_by(keyword=keyword).first()
            if index is None:
                web_page_id_scores:Dict[int, float] = {web_page_id:scores[keyword]}
                index = InvertedIndexModel(keyword=keyword, web_page_id_scores=f"{web_page_id_scores}")
            else:
                web_page_id_scores:Dict[int, float] = eval(f"{index.web_page_id_scores}")
                web_page_id_scores[web_page_id] = scores[keyword]
                index.web_page_id_scores = f"{web_page_id_scores}"
            session.add(index)
        session.commit()

    def start(self) -> None:
        self.__start_time = datetime.now()
        
        while True:
            url:Optional[str] = self.pop_url()
            if url is None:
                break

            web_page_analyzer:WebPageAnalyzer = self.request(url)
            if web_page_analyzer is None:
                continue

            id = self.update_webpage(web_page_analyzer)
            self.update_inverted_index(id, web_page_analyzer)

            urls:List[str] = web_page_analyzer.urls()
            for url in urls:
                if not self.expired(url, timedelta(seconds=config.cd)):
                    logger.info(f"{url} is cooling down, skip.")
                    continue
                self.push_url(url)

            logger.info(f"{web_page_analyzer.title()} {url} OK.")


if __name__ == "__main__":
    logger.setLevel(level=logging.DEBUG)
    console = logging.StreamHandler()
    logger.addHandler(console)
    spider = Spider()
    spider.push_urls(config.entry_urls)
    spider.start()

