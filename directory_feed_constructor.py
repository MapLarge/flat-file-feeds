"""
Classname: DirectoryFeedConstructor
Description: Creates a feed for an internal directory type of feed
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the site_feed_constructor class
"""

import os
import re
import sys
import datetime as dt
import codecs
import uuid
import shutil

from feed_constructor import FeedConstructor

class DirectoryFeedConstructor(FeedConstructor):

    """
    Define the class properties
    """

    depth_limit = None
    storage_root = None
    storage_subdirectory = None
    storage_directory = None
    web_root = None
    web_subdiretory = None
    web_directory = None
    start_directory = None
    search_filter = None

    def __init__(self, **config_json):

	"""
	Initialize the super class and load the class properties from the config json
	"""

	super(DirectoryFeedConstructor, self).__init__(**config_json)
	
   	self.storage_root = self.config_json['storage_root']
	self.storage_subdirectory = self.config_json['storage_subdirectory']
	self.storage_directory = os.path.join(self.storage_root, self.storage_subdirectory)
	self.start_directory = self.config_json['start_directory']
	self.web_root = self.config_json['web_root']
        self.web_subdirectory = self.config_json['web_subdirectory']
        self.web_directory = self.web_root + "/" + self.web_subdirectory
	
	if self.config_json['feed_type'] == 'directory':
            self.depth_limit = self.config_json['depth_limit']
            self.search_filter = self.config_json['search_filter']
	else:
	    self.depth_limit = 1
            self.search_filter = self.config_json['file']


    def walk_dir(self):

        """
        Walk the directory with a given depth_limit
        """

        path = os.path.normpath(self.start_directory)
        #If the local subdirectory for starage does not exist,
        # create it
        try:
            os.makedirs(self.storage_directory)
        except OSError:
            if os.path.exists(self.storage_directory):
                pass
            else:
                raise
        fpattern = re.compile(self.search_filter) if self.search_filter else None
        adate = dt.datetime.utcnow().isoformat()
        with codecs.open(self.storage_file, 'w', "utf-8") as ff:
            for root,dirs,files in os.walk(self.start_directory, topdown=True):
                depth = root[len(path) + len(os.path.sep):].count(os.path.sep)
                if self.depth_limit and depth == self.depth_limit:
                    
                    dirs[:] = [] # Don't recurse any deeper
                else:
                    for afile in files:
                        if fpattern and fpattern.match(afile):
                            # Want to add each entry to the file,
                            fpath_orig = os.path.join(root, afile)
                            fpath_stage = os.path.join(self.storage_directory, afile)
                            try:
                                shutil.copy(fpath_orig, fpath_stage)
                                url = self.web_directory + "/" + afile
                                ff.write('{0}, {1}, {2}\n'.format(fpath_orig,
                                                              url,
                                                              adate.encode('utf-8')))
                            except IOError as e:
                                continue
                            except Exception:
                                print e.message


    def construct_feed(self):

        """
        Execute the walk_dir method
        """

        self.walk_dir()

    def provide_params(self):

        """
        Provide parameters needed to dave the feed to the database
        """
        params = dict()
        params['title'] = self.title
        params['root_dir'] = self.start_directory
        params['items_url'] = self.storage_file
        params['feed_uuid']= uuid.uuid4()
        params['pub_time'] = dt.datetime.now()
        params['mod_time'] = dt.datetime.now()
        return params




