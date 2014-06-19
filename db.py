"""
Class: db
Description: Basic database connectivity
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the db class
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('conf/feed_service.cfg')

db_uri = config.get('ServerConfig', 'db')
engine = create_engine(db_uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()

def init_db():
    """
    Start the database engine connection
    :return:
    """
    Base.metadata.create_all(bind=engine)
