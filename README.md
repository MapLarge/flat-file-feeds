![F3 Logo](http://maplarge-public.s3.amazonaws.com/vm/flat-file-feeds/Flat-File-Feeds-logo/Flat-File-Feeds-logo-WITH-shadow-184-x-241.png)

**F3 - Flat File Feeds -** Simple Bulk Data Sharing

**Bulk Sharing:** Engineering teams often need to exchange data in bulk. The the Flat File Feeds api, or "F3" for short, defines a basic set of utilities that allow organizations to rapidly bring together and share data stores in a standardized central location. The service is intended for groups that want a simple low cost way to exchange data that may be located in "hard to reach" places: web sites that require some degree of wrangling/scraping to access, corporate databases that require additional permissions, or legacy clients to access. 

**Merge Multiple Sources:** The tool provides the ability to gather data from three sources. The web scraper provides the ability to easily scrape websites for links to files of types specified in the configuration files and then aggregate those links within a single CSV file. The directory feed presents the ability to easily expose the contents of a directory as an aggregated list of links within CSV file. The database feed provides a CSV containing the results of a user-defined SQL query.

**Extremely Simple & Lightweight:** The lightweight nature and common exchange format allows multiple integration paths through a variety of stable, mature libraries that are available to choose from for nearly any target platform. VMWare and Amazon AWS images are provided to reduce the configuration overhead and make the tools available to a wider audience. The source code is lightweight and makes use use of open source libraries. Programmers will be able to tailor the tool for their specific needs, while technical users will be able to rapidly get a vm deployed and serving feeds.

**Input:** The system accepts three data input sources and makes them all available as a consistent output format that can be updated on a configurable schedule:.

**(1) Remote Websites** : Enter a url and the system crawls the site looking for all files of a certain type and downloads them to the local file system.

**(2) Local Databases** : Enter list of SQL statements and each query is automatically exported to a flat CSV text file on the local file system.

**(3) Local Local Files** : Point the system at a local directory with a search pattern and all files are automatically indexed

**Output** : The system automatically runs a simple web service that provides two outputs (1) a bulk listing of all meta data, and (2) download urls. The key to the output is extreme simplicity designed to minimize integration costs. 

**(1) Meta Data:** The main index provides a list of data feeds which is available in 2 formats (1) a simple flat CSV text listing direct download urls and meta data for all available files, and (2) the same data in a RSS format for easy integration with other feed tools.

**(2) Download Urls** : each file is downloadable with a simple url.

**Example Usage** :

**Input:** Point F3 at ftp.census.gov and request a scrape of all files with the extension \*.shp

**Output** : example.com/Meta returns a list of urls, and each file available for download
