#!/usr/bin/env python
"""
* coding=utf8
*
* HtmlParse.py
* ------------
* This is a simple script to fetch files from a website and sorting them into matching catalogs.
* Default example uses the www.wherewhywhen.com post containing files from the Ricky Gervais show from XFM.
* All MP3 files on in the post will be downloaded to the current directory and sorted into their respective series.
*
* I am in no way responsible for any files downloaded in this example, or any potential breach of potential copyrights
* they may be associated with. If you use this code as is, you are solely responsible for any breach of creative or
* copyrights you might be engaging in.
*
"""
from BeautifulSoup import BeautifulSoup
import wgetter
import urllib2
import re
import os


__author__ = "Rene 'Zorko' Oestensen"
__copyright__ = "Copyright 2015, Zorko"
__license__ = "GPL 3.0"
__version__ = "0.1.0"
__maintainer__ = "Zorko"
__email__ = "contact@zorko.co"


def main(url):
    """
    Fetch files and catalog downloaded files
    :return:
    """
    html = urllib2.urlopen(url, timeout=5)
    soup = BeautifulSoup(html)

    for link in soup.findAll('a', attrs={'href': re.compile(".mp3")}):
        # Fetch the URL
        the_file = link.get('href')
        # Fetch the URL content
        wgetter.download(the_file)
        # Convert URL to utf-8 and get filename
        the_file_utf8 = the_file.encode('utf-8')
        file_name = re.search(r'/(Series.+\.mp3)$', the_file_utf8, re.I)
        # Move file into correct directory
        _catalog_file(file_name.group(1))

    return None


def _catalog_file(file_name):
    """
    Check file name and decide where to move said file
    :param file_name:
    :return:
    """
    # Check filename and move file to a suiting directory
    regex = re.search(r'^(Series-\d+)', file_name, re.I)
    destination = regex.group(1)

    if os.path.isdir(destination) is not True and os.path.exists(destination) is not True:
        os.mkdir(destination, 0777)

    if os.path.exists(file_name):
        os.rename(file_name, '%s/%s' % (destination, file_name))
        return True

    return False


if __name__ == '__main__':
    main('http://www.wherewhywhen.com/xfm-the-ricky-gervais-show-seasons-1-4-complete/')
