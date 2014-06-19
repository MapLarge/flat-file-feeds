__author__ = 'charlescearl'
"""
Implements a service that will process  basic feed 
management and display
"""
from urlparse import urljoin
from flask import Flask
from werkzeug.contrib.atom import AtomFeed
import feed_manager as fm
from db import init_db
from flask import request
import ConfigParser


init_db()

app = Flask(__name__, static_url_path='/static')

def make_external(url):
    return urljoin(request.url_root, url)


@app.route("/")
def hello():
    return "Basic Feed Service"

@app.route('/feeds')
def get_feed():
    """
    Get the named feed and display all of the items.
    If the name is not given, return all.
    """
    feed = AtomFeed('Maplarge data feed',
                    feed_url=request.url, url=request.url_root)
    
    rt = request.url_root
    if 'title' in request.args:
        (status, single_feed) =  fm.get_rss_feed(request.args['title'], root=rt)
        if status:
            return single_feed
        return ("Could not processes creation request", 500)
    (status, feeds) =  fm.get_rss_feeds(feed, root=rt)
    if status:
        return feeds
    return ("Malformed feed creation request", 500)
    


if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read('conf/feed_service.cfg')
    port = config.getint('ServerConfig', 'port')
    host = config.get('ServerConfig', 'host')
    app.run(debug=True, port=port, host=host)
