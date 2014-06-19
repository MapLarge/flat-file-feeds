"""
Module: feed_def_reader
Description: Reads in fed def file and controls the feed construction process
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the feed_def_reader module
"""

import json
import sys

from website_feed_constructor import WebsiteFeedConstructor
from directory_feed_constructor import DirectoryFeedConstructor
from db_feed_constructor import DatabaseFeedConstructor

def construct_feeds_from_defs(filename):

    """
    Read in the feed definition file, return a list of feed definitions and construct a feed for each definition
    """

    js = None
    with open(filename) as fp:
        js = json.load(fp)
    assert js
    assert 'feeds' in js
    return [ construct_feed(feed) for feed in js['feeds'] ]

def construct_feed(feed):

    """
    Instantiate a particular feed object and create the feed
    """
    
    feed_type = feed['feed_type']
    feed_instance = None
    if feed_type == 'directory':
        feed_instance = DirectoryFeedConstructor(**feed)
	                                
    elif feed_type == 'website':
        feed_instance = WebsiteFeedConstructor(**feed)
	
    elif feed_type == 'database':
        feed_instance = DatabaseFeedConstructor(**feed)

    elif feed_type == 'file':
	feed_instance = DirectoryFeedConstructor(**feed)

    else:
        print "Invalid feed type specified"

    return feed_instance
    
 
