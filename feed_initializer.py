"""
Module: feed_initializer
Description: Reads in fed def file and controls the feed construction process
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the feed_initializer module
"""

import os.path
import feed_def_reader as fdr
import time
from feed_manager import update_feed
import argparse

def build_feeds(feed_def):

    """
    Read in the configuration file with the feed_def_reader module and construct the feed with its appropriate class
    """

    feeds = fdr.construct_feeds_from_defs(feed_def)
    
    pid = None
    for feed in feeds:
        pid = os.fork()
        print "Constructing feed {0}".format(feed)
        if pid == 0:
            time.sleep(10)
            if feed:
                feed.construct_feed()
                update_feed(feed.provide_params())
                time.sleep(60)
                os._exit(0)
    os.wait()


def main():

    """
    Read the command argument and execute the build_feeds method with the argument
    """
    
    parser = argparse.ArgumentParser(description='Create feeds.')
    parser.add_argument('--defs', '-d', help='feed definition file', required=True)
    args = parser.parse_args()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    build_feeds(args.defs)


if __name__ == '__main__':
    main()
