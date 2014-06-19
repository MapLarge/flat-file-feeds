"""
Classname: FeedConstructor
Description: Creates a feed for an website type of feed
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the site_feed_constructor class
"""
from xml.dom import minidom

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader import XPathItemLoader
from scrapy import log

import subprocess as sp
import re
import os
import uuid
import datetime
import urllib

from feed_constructor import FeedConstructor

class WebsiteFeedConstructor(CrawlSpider, FeedConstructor):

    """
    Define the class properties
    """

    name = "Data_Feed"
    start_urls = ['http://www.cnn.com/']
    allowed_domains = ['cnn.com']
    depth_limit = ''
    search_filter = ''
    rules = [
		Rule(SgmlLinkExtractor(allow=('')), callback='parse_item'),
		Rule(SgmlLinkExtractor(allow=('')), follow=True)
	    ]
    

    def __init__(self, *args, **kwargs):

	"""
	Initialize the super class, connect the spider arguments to the dynamic variables and load the class properties from the config json
	"""
	
	FeedConstructor.__init__(self, **kwargs)
	kwargs = {}
	super(WebsiteFeedConstructor, self).__init__(*args, **kwargs)
	
	self.name = str(self.config_json.get('name', 'Missing value'))
	self.search_filter = str(self.config_json.get('search_filter', 'Missing value'))
	self.start_urls = str(self.config_json.get('start_urls', 'Missing value')).split(",")
	print self.start_urls
	#self.allowed_domains = str(self.config_json.get('allowed_domains', 'Missing value')).split(",")
	#self.rules = [
	#	Rule(SgmlLinkExtractor(allow=(self.search_filter)), callback='parse_item'),
	#	Rule(SgmlLinkExtractor(allow=('')), follow=True)
	#   ]
	self.depth_limit = self.config_json.get('depth_limit', 'Missing value')

    def construct_feed(self):
        """
        Execute a scrapy crawl spider with the provided arguments
        """
	
	exec_list = ["scrapy", "runspider", "website_feed_constructor.py", "-s", "DEPTH_LIMIT="+self.depth_limit, "-s", "FEED_FORMAT=CSV", "-s", "FEED_URI="+self.storage_file, "-s", "LOG_FILE="+self.log_file ]

        try:
            val = sp.check_output(exec_list)
        except sp.CalledProcessError as cpe:
            self.log("Launch failure", level='ERROR', )

 
    def provide_params(self):

        """
        Provide parameters needed to dave the feed to the database
        """

        params = dict()
        params['title'] = self.title
        params['root_url'] = self.start_urls
        params['items_url'] = self.storage_file
        params['feed_uuid']= uuid.uuid4()
        params['pub_time'] = datetime.datetime.now()
        params['mod_time'] = datetime.datetime.now()
        return params


    def parse_item(self, response):

	"""
	Parse the scraped item and add the values to the link item collection
	"""

 	hxs = HtmlXPathSelector(response)

	l = LinkLoader(LinkItem(), hxs)
	l.add_value('name', self.name)
	l.add_value('title', self.title)
	l.add_value('website', self.start_urls)
        l.add_value('url', response.url)
        
	return l.load_item()


"""
Classname: LinkItem
Description: the data pattern class for storing scraped items from targeted websites
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

class LinkItem(Item):
    name = Field()
    title = Field()
    website = Field()
    url = Field()


"""
Classname: LinkLoader
Description: helper class for extracting XPathItems and loading them for output
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

class LinkLoader(XPathItemLoader):
    default_output_processor = TakeFirst()





        




