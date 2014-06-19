"""
Classname: DirectoryFeedConstructor
Description: Creates a feed for a database type of feed
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the site_feed_constructor class
"""

import os
import psycopg2
import datetime
import uuid
from feed_constructor import FeedConstructor

class DatabaseFeedConstructor(FeedConstructor):

    """
    Define the class properties
    """

    user = None
    db = None
    host = None
    query = None
    table = None
    uri = None
    
    def __init__(self, **config_json):

	"""
	Initialize the super class and load the class properties from the config json
	"""

        super(DatabaseFeedConstructor, self).__init__(**config_json)
	
	self.uri = self.config_json['uri']
        self.host = self.config_json['host']
        self.query = self.config_json['query']
        self.user = self.config_json['user']
        self.table = self.config_json['table']
	self.db = self.uri.split("/")[-1] if self.uri else self.db

    def dump_db_table(self):

        """
        Constructs a csv feed dump from the associated database
        """

        if self.uri:
            conn = psycopg2.connect(self.uri)
        else:
            conn = psycopg2.connect(database=self.db,
                                    user=self.user,
                                    host=self.host)
        cur = conn.cursor()
        cur.execute(self.query)
        ff_name = self.storage_file
  
        with open(ff_name, "w") as ff:
            for res in cur.fetchall():
                ff.write(", ".join(map(lambda x: str(x), res))+'\n')

    def construct_feed(self):
	""" 
	Execute the dub_db_table method
	"""
        self.dump_db_table()

    def provide_params(self):

        """
        Provide parameters needed to dave the feed to the database
        """

        params = dict()
        params['title'] = self.title
        params['database_source'] = self.db
        params['items_url'] = self.storage_file
        params['table_name'] = self.table
        params['feed_uuid']= uuid.uuid4()
        params['pub_time'] = datetime.datetime.now()
        params['mod_time'] = datetime.datetime.now()
        return params



