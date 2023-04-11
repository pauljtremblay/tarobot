#!/usr/bin/env python3

from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from tarobot.app import config

db, pool = config.db, config.db.pool
encoded_pass = quote_plus(db.password)
db_url = "{}+{}://{}:{}@{}:{}/{}".format(db.dialect, db.driver, db.user, encoded_pass, db.host, db.port, db.schema)
engine = create_engine(db_url, pool_size=pool.size, pool_recycle=pool.recycle_secs, pool_timeout=pool.timeout_secs)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()
