"""
Provides a structure for storing the data to be placed into
feed files.
"""
from scrapy.item import Item, Field

class FeedFileItem(Item):
    """ Provides a container for storage of the data from
    which to create a feed file.
    """
    url = Field()
    creation_time = Field()
    author = Field()
    file_type = Field()
    metadata = Field()
    
