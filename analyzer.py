#! /usr/bin/env python3

from bs4 import BeautifulSoup
import jieba
from urllib.parse import urlparse, ParseResult
from typing import List, Dict

class WebPageAnalyzer(object):
    def __init__(self, url:str, html:str) -> None:
        self.__url:str = url
        self.__html:str = html.replace('\0', '')
        self.__bs = BeautifulSoup(self.__html, "lxml")

    def url(self) -> str:
        return self.__url

    def title(self) -> str:
        if self.__bs.title is not None:
            return self.__bs.title.getText().strip()

    def text(self) -> str:
        return self.__bs.getText() 

    def content(self) -> str:
        return self.__html

    def keywords(self) -> List[str]:
        words = jieba.cut_for_search(self.text())
        return [word.lower() for word in words if len(word) < 1024 and word.strip() != "" and word not in "`~!@#$%^&*()_+-={[]}\\|\"':;,.?/，。、·"]

    def keyword_scores(self) -> Dict[str, float]:
        keywords:List[str] = self.keywords()
        scores:Dict[str, float] = {}
        for keyword in keywords:
            if keyword not in scores:
                scores[keyword] = 1
            else:
                scores[keyword] += 1
        return {key:scores[key]/len(scores) for key in scores}


    def urls(self) -> List[str]:
        refer_url:ParseResult = urlparse(self.__url)
        doc = BeautifulSoup(self.__html, "lxml")
        anchors = doc.find_all('a')
        urls:Set[str] = set()
        for anchor in anchors:
            try:
                url:ParseResult = urlparse(anchor.get("href"))
            except Exception as e:
                logging.warning(e)
                continue
            if url.scheme == "":
                url = url._replace(scheme=refer_url.scheme)
            if url.netloc == "":
                url = url._replace(netloc=refer_url.netloc)
            urls.add(str(url.geturl()))

        return urls



if __name__ == "__main__":
    web_page_analyzer = WebPageAnalyzer(url="", html="<html><head><title> 葡萄Grape </title></head><body>吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮</body></html>")
    print(web_page_analyzer.keyword_scores())