import shutil
from sqlalchemy import func
from model import DBSession, WebPageModel, InvertedIndexModel, SpiderQueueModel
import cpuinfo
import platform

cpu = cpuinfo.get_cpu_info()
uname = platform.uname()

def node() -> str:
    return uname.node

def system() -> str:
    return uname.system

def release() -> str:
    return uname.release

def machine() -> str:
    return uname.machine

def python_version() -> str:
    return cpu["python_version"]

def cpu_name() -> str:
    return cpu["brand_raw"]

def cpu_freq() -> str:
    return cpu["hz_actual_friendly"]

def web_page_count() -> int:
    session = DBSession()
    return session.query(func.count(WebPageModel.id)).scalar()

def inverted_index_count() -> int:
    session = DBSession()
    return session.query(func.count(InvertedIndexModel.id)).scalar()

def spider_queue_count() -> int:
    session = DBSession()
    return session.query(func.count(SpiderQueueModel.id)).scalar()

def disk_usage() -> int:
    return round(shutil.disk_usage("/").used / (1024*1024*1024), 2)

def disk_total() -> int:
    return round(shutil.disk_usage("/").total / (1024*1024*1024), 2)