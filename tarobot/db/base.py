#!/usr/bin/env python3

"""This module serves as a base class for all sqlalchemy entity classes. Used to establish database transactions."""

from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .. app.config import CONFIG

db, pool = CONFIG.db, CONFIG.db.pool
encoded_pass = quote_plus(db.password)
db_url = f"{db.dialect}+{db.driver}://{db.user}:{encoded_pass}@{db.host}:{db.port}/{db.schema}"
engine = create_engine(db_url, pool_size=pool.size, pool_recycle=pool.recycle_secs, pool_timeout=pool.timeout_secs)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    """Establishes and returns an open session from the associated connection pool."""
    Base.metadata.create_all(engine)
    return _SessionFactory()
