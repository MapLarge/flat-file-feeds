F3 - Flat File Feeds - Simple Bulk Data Sharing
========

#   Overview

The Flat File Feeds (F3) defines a basic set of utilities that benefit collaborative information machine by allowing organizations to rapidly share large data stores in accessible data formats. We use Atom as a means of pointing to each feed, while the bulk of the shared data gets provided as csv. The Feed Service is intended for groups that want to exchange data that may be located in "hard to reach" places: web sites that require some degree of wrangling/scraping to access, corporate databases that require additional permissions or legacy clients to access, etc.

Users of the Feed Service define how to construct feeds from internal databases, directory hierarchies, and websites. These feeds are then published using a webservice that allows third parties to access the data.

Thus, our distribution contains **feed initializer** scripts that help the user build feeds by defining **feed definitions.** The feed builder is accompanied by a **feed service** that publishes information about each feed through using the Atom syndication format. All of the code is written in Python. It uses [Flask](http://flask.pocoo.org/)(for feed serving), [scrapy](http://scrapy.org/)(for web site scraping), and [SQLAlchemy](http://www.sqlalchemy.org/)for database feed creation.

This initial release of F3 provides very basic capabilities and is limited in scope:

1. The code is configured for a Linux Ubuntu 14 distribution.
2. The only database support currently implemented is Postgres.

# 
# Quick Start

## 
# Setting up the VM

The zip file contains a VMware virtual machine. Unzip all of the files to your virtual machine datastore. Using the VMWare interface, add this virtual machine to your inventory and start the server. The default user name is: user and the password is: password.

Also available is an Amazon Web Services AMI. This AMI is located in the US east region with number: XXXXX. Create a new instance of this AMI in your EC2 account and start the instance. You can then use any SSH client to log into the instance.

The server is preconfigured for all functionality (security, ports, postgres, scrapy, python and all other dependencies). There are two main configuration tasks to set the machine up for its IP within your environment.

First, the server's IP address is set to 192.168.1.7 by default with a gateway and DSN of 192.168.1.5. You will need to log into the Ubuntu system settings and change the IP, gateway and DSN to values that will work in your network.

Second, the server is configured to use port 5010 for the feed service. If this port is not good for your environment, you will need to edit the /conf/feed\_service.cfg file and change the port=5010 line to a port value that is acceptable. Once the value has been changed, simply reboot the server and the feed service will be active on the new port.

The solution is installed in the root at: /data\_feed. The default directory structure includes five subfolders. The conf folder contains all of the configuration information for the data\_feed application as well as the sample feed definition json files. The sources folder contains all of the sample data for the file and directory feed definition sample json files. The staticfolder is the target storage file location for all of the feeds created in the sample feed definition json files. The log folder is the target log file location for all of the feeds created in the sample feed definition json files. The sock folder is the location for storage of the socket file for communication between Flask, Uwsgi, and Nginx.

# 
# Setting up feed definition files

A JSON configuration file specifies how to construct each of the feeds provided by the service. There server supports four different feed types:

1. Website – any internal or external website can be a target to be scraped for data.
2. Directory – any internal folder structure can be crawled for data.
3. Database – any Postgres database can be queried for data.
4. File – any individual file can be a target for data. 

There is a sample of each type of feed definition file located in the /data\_feed/conf directory. Each files shows sample data that is configured for the VM and illustrates all of the required variables used for each feed type.

conf/feed\_def\_website.json

conf/feed\_def\_directory.json

conf/feed\_def\_database.json

conf/feed\_def\_file.json

## 
# Shared Parameters

## Every feed definition file shares a number of parameters. The parameters unique to each feed type are listed with the example and feed type below. The common parameters shared by all types of feed definitions are:

## **feed\_type:** required and must be the keyword specific to the type of feed being created.

##     (usage – starting the correct type of feed constructor)

## **title:** any descriptive title you would like to use.

##     (usage – descriptive reference saved in the meta data database for referencing this feed in the future)

## **storage\_file:** any folder and file name for storing the scraped data links (the path is relative to the application base folder).

##     (usage – used by scrapy to create the export CSV file where the items are stored)

## **log\_file:** any folder and file name for storing the execution log information (the path is relative to the application base folder).

##     (usage: - used by scrapy to record the history of activities, it is cumulative)

## 
# Website

Sample feed definition file contents:

{"feeds":

[{"feed\_type" : "website",

  "name": "Web Name",

  "title": "Web Title",

  "storage\_file": "static/website.csv",

  "log\_file": "log/website.log",

  "allowed\_domains": "msn.com",

  "start\_urls": "http://www.msn.com/",

  "depth\_limit": "4",

  "search\_filter": ""}]}

## **feed\_type:** required and must be the keyword "website" 

##     (usage – starting the correct type of feed constructor)

## **allowed\_domains:** comma separated list of domain names (i.e. "cnn.com" or "cnn.com, msn.com")

##     (usage – provides scrapy a set of domain names that are allowed in the spider execution)

## **start\_urls:** comma separated list of websites names (i.e. "http://www.cnn.com/" or "http://www.cnn.com, http://www.msn.com")

##     (usage – provides scrapy a set of websites that are to be targeted in the spider execution)

## **depth\_limit:** integer value indicating the depth to query the websites

##     (usage: - limits scrapy to this number of links of depth when the spider crawls the websites)

## **search\_filter:** regular expression to filter out what types of files to return in the scraping

##     (usage: - limits the returned files to only those found in the regular expression)

## 
# Database

Sample feed definition file contents:

{"feeds":

[{"feed\_type" : "database",

  "title": "SampleServer",

  "storage\_file": "/data\_feed/static/db.csv",

  "log\_file": "/data\_feed/log/log/db.log",

  "user": "user",

  "db": "public",

  "table": "mytable",

  "host": "localhost",

  "uri": "postgres://user:password@localhost",

  "query": "select \* from mytable"}]}

## **feed\_type:** required and must be the keyword "database".

##     (usage – starting the correct type of feed constructor)

## **user:** username for logging into the database.

##     (usage – used by the database connection service to authenticate)

## **db:** database name to access for the feed data.

##     (usage – used by the database connection service to set the target database)

## **table:** table name to access for the feed data..

##     (usage – used by the database connection service to set the target table)

## **host:** server name where the database resides.

##     (usage – used by the database connection service to connect to the database service)

## **uri:** postgres connection string.

##     (usage – used by the database connection service to connect to the database service)

## **query:** sql query to execute to retrieve feed data from the database.

##     (usage – used by the database connection service to return data from the database for the data feed)

## 
# Directory

Sample feed definition file contents:

{"feeds":

[{"feed\_type" : "directory",

  "title": "SampleServer",

  "storage\_file": "static/directory.csv",

  "log\_file": "log/directory.log",

  "start\_directory": "/data\_feed/sources",

  "storage\_root": "/data\_feed/static",

  "storage\_subdirectory": "./directory\_feed",

  "search\_filter" : ".\*\\.pdf",

  "depth\_limit": "2",

  "web\_root": "http://localhost/data",

  "web\_subdirectory": "directory\_feed"}]}

## **feed\_type:** required and must be the keyword "directory".

##     (usage – starting the correct type of feed constructor)

## **start\_directory:** directory location to target as the base directory to search.

##     (usage – used by the directory search as the base location from which to start the search)

## **storage\_root:** base directory for all files found in the directory search to be copied for serving through the data feed.

##     (usage – used by the directory search as the base feed location)

## **storage\_subdirectory:** the subdirectory within the base storage\_root to use for this particular feed.

##     (usage – used by the directory search as the unique folder for this feed)

## **depth\_limit:** integer value indicating the depth to query the websites

##     (usage: - limits scrapy to this number of links of depth when the spider crawls the websites)

## **search\_filter:** regular expression to filter out what types of files to return in the scraping

##     (usage: - limits the returned files to only those found in the regular expression)

## **web\_root:** base directory used by the feed service for serving the files in the webserver.

##     (usage – used by the directory search as the base website feed location)

## **web\_subdirectory:** the subdirectory within the base web\_root to use for this particular feed.

##     (usage – used by the directory search as the unique website folder for this feed)

## 
# File

Sample feed definition file contents:

{"feeds":

[{"feed\_type" : "file",

  "title": "SampleServer",

  "storage\_file": "static/file.csv",

  "log\_file": "log/file.log",

  "start\_directory" : "/data\_feed/sources",

  "storage\_root": "/data\_feed/static",

  "storage\_subdirectory": "./file\_feed",

  "file" : "filesample.csv",

  "web\_root": "http://localhost/data",

  "web\_subdirectory": "file\_feed"}]}

## **feed\_type:** required and must be the keyword "file".

##     (usage – starting the correct type of feed constructor)

## **start\_directory:** directory location to target as the base directory to search.

##     (usage – used by the file feed as the base location from which to start the search)

## **storage\_root:** base directory for all files found in the directory search to be copied for serving through the data feed.

##     (usage – used by the file feed as the base feed location)

## **storage\_subdirectory:** the subdirectory within the base storage\_root to use for this particular feed.

##     (usage – used by the file feed as the unique folder for this feed)

## **file:** name of the file to source

##     (usage: - limits the returned file to the item matching this filename)

## **web\_root:** base directory used by the feed service for serving the files in the webserver.

##     (usage – used by the file feed as the base website feed location)

## **web\_subdirectory:** the subdirectory within the base web\_root to use for this particular feed.

##     (usage – used by the file feed as the unique website folder for this feed)

# 
# Creating and serving feeds

Now that you have defined the feeds that you want to serve with the JSON feed definition files, the next step is to "initialize" the feeds into the feed server. The current implementation provides a command line interface for "initializing" the feeds, but the code could easily be extended to schedule the commands to execute on a schedule as well.

When the feed\_initializer is executed, the module reads the specified feed definition and stores the meta data in a Postgres database. Depending on the feed type, the feed initializer may also store files in an interim directory structure as well.

Once a feed has been initialized, the feed\_service reads the feed meta data from the Postgres database and serves up the links via a web service which provides access to the feeds.

## 
# Creating feeds from definitions

The feed\_initializermodule loads the feed definition file, calls a helper modulefeed\_def\_readerto parse the file and create: WebsiteFeedConstructor , DirectoryFeedConstructor , DatabaseFeedConstructor, instances. Each of these classes inherits from the FeedConstructorclass which provides all common feed functionality. Each constructor will create a feed in the database that correspond to each feed as well as saving a CSV file with the results of the feed construction for use in serving up the Atom feed.

The command line for creating a feed is the "feed\_initializer.py" file and takes a single argument with the – d . Below, the first example runs the included website scraping sample.

user@ubuntuvm:~/data\_feed$ python feed\_initializer.py –d conf/feed\_def\_website.json

user@ubuntuvm:~/data\_feed$ python feed\_initializer.py –d 

1. Web Site Feeds.Here,feed\_initializerwill launch a scrapy crawler to assemble the feed files from the data sources. Each item discovered during the crawl (e.g. xls file link) will be stored as a row in a csv file. The crawling process will then create a single feed data base entry that will link to the csv file. The scrapy crawler is defined in modulewebsite\_feed\_constructor. This module is called in a shell invocation inside of feed\_initializer. The modulewebsite\_feed\_constructorcreates the file in which the crawled items are stored. After the process completes,feed\_initializerwrites an entry to the database tableFeed(defined in modulemodels)

The entry will have structure

  title, root\_uri, items\_url

Wheretitleis the name given the feed,root\_urlwill be the url of the root of the page anditems\_urlis the location of the file in which the items are stored.

1. Directory Feeds.Here,feed\_initializerwill launch a process in which an instance of DirectoryFeedConstructorruns to construct a csv that lists the contents of a specified directory. After the process completes,feed\_initializerwrites an entry to the database tableFeed(defined in modulemodels)

The entry will have structure

  title, root\_dir, items\_url

For directory feed entries, the convention is to link each directory line to a hosting location. That is

  , 

By convention the definition of the file feed prescribes where to place the files stored by a particular directory feed and where to serve them from

1. Database Feeds. Here,feed\_initializerwill launch a process in which an instance ofDatabaseFeedConstructorruns to construct a csv that lists the contents of a query specified in the configuration file. After the process completes,feed\_initializerwrites an entry to the database tableFeed(defined in modulemodels)

The entry will have structure

  title, database\_source, items\_url

where the database\_source is of the form database:table. For the time being, the interface only supports postgres, but can be readily extended to support other databases supported by the PythonSQLAlchemylibrary.

## 
# Accessing the feed data

The user gets a listing of the feeds by using thefeedsGET query. For example, if the site is on home.com,

http://home.com/feeds

A user requests a specific feed by issuing the GET queryfeed/. For example

http://home.com/feed/ThisIsMyFeedTitle
