"""
Classname: FeedConstructor
Description: Base class for defining how feeds are generated.  Handles the import of the config json file.
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the feed_constructor class
"""

import os
import json

class FeedConstructor(object):

    """
    Define the class properties
    """

    title = None
    storage_file = None
    log_file = None
    config_json = {}

    
    def __init__(self, **config_json):

	"""
	Extract the json and initialize the common feed properties
	"""
	self.config_json = config_json
	self.title = str(self.config_json.get('title', 'Missing value'))
        self.storage_file = str(self.config_json.get('storage_file', 'Missing value'))
        self.log_file = str(self.config_json.get('log_file', 'Missing value'))


	
