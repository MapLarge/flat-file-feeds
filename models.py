"""
Class: feed
Description: Defines all of the database fields used for saving a feed.
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the feed class
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flask import json
from db import Base
import datetime as dt

def now():
    return dt.datetime.utcnow().replace(microsecond=0)

class Feed(Base):

    """
    Feed fields list
    """

    __tablename__ = 'feeds'
    feed_id = Column(Integer, primary_key=True)
    title = Column(String(50), unique= True)
    items_url = Column(String(100))
    root_url = Column(String(100))
    root_dir = Column(String(100))
    database_source = Column(String(100))
    table_name = Column(String(100))
    file_source = Column(String(100))
    feed_uuid = Column(UUID(as_uuid=True))
    pub_time = Column(DateTime())
    mod_time = Column(DateTime())
    

    def __init__(self, title=None, items_url=None, database_source=None,
                 root_dir=None,
                 file_source=None, root_url=None,
                 database_name=None, table_name=None,
                 feed_uuid=None, mod_time=None, pub_time=None):
        """
        Setup the feed with a title
        :rtype : object
        """
        self.title = title
        self.items_url = items_url
        self.database_source = database_source
        self.file_source = file_source
        self.root_url = root_url
        self.root_dir = root_dir
        self.database_name = database_name
        self.table_name = table_name
        self.feed_uuid = feed_uuid
        self.mod_time = mod_time
        self.pub_time = pub_time

    def __repr__(self):
        """
        Print representation of the feed
        """
        return '<Feed %r>' % (self.title)


    def to_json(self):
        """
        Return a json string of the feed
        """
        return json.jsonify(title=self.title, feed_id=self.feed_id)


