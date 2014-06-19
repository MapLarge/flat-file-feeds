"""
Module: feed_manager
Description: Basic feed management for the atom rss feed.
Authored by: MapLarge, Inc. (Scott Rowles)
Change Log: 
"""

"""
Define all the imports for the feed_manager module
"""

from sqlalchemy.exc import IntegrityError

import sqlite3
from db import init_db
from db import db_session
from flask import json
from models import Feed
import datetime
import uuid

def create_feed(name, session=None):
	"""
	Return the named feed
	"""
	local_session = None
	created = None
	feed = None
	if not session:
		local_session = db_session()
	else:
		local_session = session
	feed = retrieve_feed(name, local_session)
	if feed:
		return (True, feed)
	try:
		feed = Feed(title=name)
		local_session.add(feed)
		local_session.commit()
		created = True
	except Exception as e:
		print "Got exception {0}".format(e)
		feed = None
		local_session.rollback()
	finally:
		if not session:
			local_session.close()
		return (created, feed)


def update_feed(feed_params, session=None):
	"""
        Updates the feed object described by feed_params
        Arguments:
          feed_params: string json formatted string that describes the 
           parameters of the feed object to create.
          session: sqlalchemy.orm.session.Session will be the session object
           to interact with the database
	"""
	local_session = None
	created = None
	feed = None
	if not session:
		local_session = db_session()
	else:
		local_session = session
	try:
		feed = Feed(**feed_params)
		existing_feed = local_session.query(Feed).filter(Feed.title == feed.title).first()
		if existing_feed:
			update_param = dict()
			print "Updating feed {0}".format(existing_feed)
			for key, value in feed_params.iteritems():
				if key != 'pub_time' and key != 'feed_uuid':
					update_param[key] = value
				elif key == 'pub_time':
					update_param[key] = existing_feed.pub_time
				else:
					update_param[key] = existing_feed.feed_uuid
			print update_param
			local_session.query(Feed).filter(Feed.title == feed.title).update(update_param)
		else:
			local_session.merge(feed)
		local_session.commit()
		created = True
	except Exception as e:
		print "Got exception {0}".format(e)
		feed = None
		local_session.rollback()
	finally:
		if not session:
			local_session.close()
		return (created, feed)


def retrieve_feed(name, session):
	"""
	Determine if the named feed is stored and if so returnn
	"""
	query = session.query(Feed).filter(Feed.title == name)
	feed = query.first()
	return feed

def get_feed(name, root=None):
	"""
	Query the engine on the feed and return the subfeeds
	if they exist
	"""
	retrieved = None
	result_string = None
	session = None
	a_feed = None
	try:
		session = db_session()
		a_feed = retrieve_feed(name, session)
		if a_feed:
			jsonified_feeds = _jsonify_feed(a_feed, root=root)
			retrieved = True
			result_string = json.dumps(jsonified_feeds, sort_keys=True,
			                           indent=4, separators=(',', ': '))
	except Exception as e:
		print e
		if not session:
			result_string = "Probably could not initiate session"
		elif a_feed:
			result_string = "Another problem encounter with feed {0}".format(a_feed)
		else:
			result_string = "Another problem encounter, session was {0}".format(session.info)
		retrieved = True
	finally:
		if session:
			session.close()
		return (retrieved, result_string)

def _jsonify_feed(feed, root=None):
	"""
	Get a json representation of the given feed
	"""
	jsonified_feeds = [fd.to_dict() for fd in feed.sub_feeds]
	jsonified_feed = {'title': feed.title, 'subfeeds': jsonified_feeds}
	jsonified_feed['root_url'] = feed.root_url
	jsonified_feed['root_dir'] = feed.root_dir
	jsonified_feed['items_url'] = feed.items_url
	if root:
		jsonified_feed['items_url'] = root+'static/'+jsonified_feed['items_url']
	return jsonified_feed


def get_feeds(root=None):
	"""
	Return all of the feeds
	"""
	session = db_session()
	feed_list = list()
	retrieved = None
	result_string = None
	for feed in session.query(Feed):
		feed_list.append(_jsonify_feed(feed, root=root))
	if len(feed_list) > 0:
		retrieved = True
		result_string = json.dumps(feed_list, sort_keys=True,
		                           indent=4, separators=(',', ': '))
	session.close()
	return (retrieved, result_string)

def get_rss_feeds(atom_feed, root=None):
	"""
	Return the result set in RSS format
	"""
	dt = datetime.datetime.utcnow()
	session = db_session()
	url_root = ''
	retrieved = None
	if root:
		url_root = root+'static/'
	result_set = session.query(Feed)
	if result_set:
		retrieved = True
		for feed in result_set:
			content = None
			if feed.database_source:
				content = "database:{0},table:{1}".format(feed.database_source,
				                                          feed.table_name)
			else:
				content = feed.root_url or feed.root_dir
			atom_feed.add(feed.title, content=content, url=url_root+feed.items_url,
			              updated=feed.mod_time, published=feed.pub_time,
			              id=feed.feed_uuid)
	session.close()
	return (retrieved, atom_feed)

def get_rss_feed(title, atom_feed, root=None):
	"""
	Return the result set in RSS format
	"""
	session = db_session()
	url_root = ''
	retrieved = None
	if root:
		url_root = root+'static/'
	feed = session.query(Feed).filter_by(title=title).first()
	if feed:
		retrieved = True
		content = None
		if feed.database_source:
			content = "database:{0},table:{1}".format(feed.database_source,
				                                      feed.table_name)
		else:
			content = feed.root_url or feed.root_dir
		atom_feed.add(feed.title, content=content, url=url_root+feed.items_url,
			          updated=feed.mod_time, published=feed.pub_time,
			          id=feed.feed_uuid)
	session.close()
	return (retrieved, atom_feed)


def destroy_feed(name):
	"""
	Destroy the given feed.
	"""
	session = db_session()
	a_feed = retrieve_feed(name, session)
	result_string = None
	if a_feed:
		try:
			session.delete(a_feed)
			session.commit()
			result_string = json.jsonify(result="destroyed_feed", target=name)
		except Exception as e:
			session.rollback()
		finally:
			session.close()
			return result_string
	return result_string





