import os
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from threading import Lock
import config

Base = declarative_base()

class WebPageModel(Base):
    __tablename__ = 'web_page'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, index=True, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    like = db.Column(db.Integer, default=0)
    hate = db.Column(db.Integer, default=0)


class InvertedIndexModel(Base):
    __tablename__ = 'inverted_index'
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.Text, unique=True, index=True, nullable=False)
    web_page_id_scores = db.Column(db.Text)

class SpiderQueueModel(Base):
    __tablename__ = 'spider_queue'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, unique=True, index=True, nullable=False)

# 初始化数据库连接:
sql_url = config.sql_url
engine = db.create_engine(sql_url)
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
DBSession = scoped_session(session_factory)