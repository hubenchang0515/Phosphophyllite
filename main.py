#! /usr/bin/env python3

from datetime import datetime
import flask
from flask import request, render_template
import threading

import config
import info
from spider import Spider
from search import Searcher

app = flask.Flask(__name__)

@app.route("/")
def index():
    print(f"=========================================================")
    return render_template("index.html", 
                            node=info.node(),
                            python_version=info.python_version(),
                            system=info.system(), 
                            release=info.release(), 
                            machine=info.machine(),
                            cpu_name=info.cpu_name(),
                            cpu_freq=info.cpu_freq(),
                            web_page_count=info.web_page_count(),
                            inverted_index_count=info.inverted_index_count(),
                            disk_usage=info.disk_usage(),
                            disk_total=info.disk_total())

@app.route("/api/search")
def search():
    query:str = request.args.get(key='query', type=str)
    page:int = request.args.get(key='page', type=int, default=0)
    page_size:int = request.args.get(key='page_size', type=int, default=20)
    searcher = Searcher()
    results = searcher.search(query)
    data = results.dumps(page=page, page_size=page_size)
    return data, 200, {"Content-Type":"application/json"}

@app.route("/preview/search")
def preview_search():
    query:str = request.args.get(key='query', type=str)
    page:int = request.args.get(key='page', type=int, default=0)
    page_size:int = request.args.get(key='page_size', type=int, default=20)
    searcher = Searcher()
    results = searcher.search(query)
    search_result_page = results.dump(page=page, page_size=page_size, exclude={"content"})
    return render_template("search.html", search_result_page=search_result_page)


def run_spier():
    spider = Spider()
    if info.spider_queue_count() == 0:
        spider.push_urls(config.entry_urls)
    spider.start()
    

if __name__ == "__main__":
    spider_thread = threading.Thread(target=run_spier)
    spider_thread.start()

    app.run(host=config.host, port=config.port, debug=config.debug)