#!/usr/bin/env python3

# This file is a part of ytlist v1.0.0
#
# Copyright (C) 2017, Slava <freeprogs.feedback@yandex.ru>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Load urls and information for videos in a video list on YouTube.

For the YouTube url with video list loads triples (url, time, title)
and prints them in format:

url time title\\n
url time title\\n
...

Example:

In:
ytlist https://www.youtube.com/playlist?list=ABCD

Out:
https://www.youtube.com/watch?v=123 1:01:01 Text of the title1
https://www.youtube.com/watch?v=456 2:02:02 Text of the title2
https://www.youtube.com/watch?v=789 3:03:03 Text of the title3

"""

__version__ = '1.0.0'
__date__ = '3 June 2018'
__author__ = 'Slava <freeprogs.feedback@yandex.ru>'
__license__ = 'GNU GPLv3'

import sys
import argparse
import urllib.request
import lxml.html

def get_charset(data):
    """Get content charset from HTTP response."""
    return data.headers.get_content_charset() or 'latin1'

def load_page(url):
    """Load HTTP-page from given url."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Firefox'})
    data = urllib.request.urlopen(req)
    charset = get_charset(data)
    return data.read().decode(charset)

def find_url_blocks(text):
    """Search in text all video blocks with video metadata."""
    doc = lxml.html.fromstring(text)
    out = [lxml.html.tostring(i, encoding='unicode')
           for i in doc.xpath(r'//tr[contains(@class,"pl-video")]')]
    return out

def parse_block(text):
    """Extract url, time and title from text."""
    doc = lxml.html.fromstring(text)
    url = ('https://www.youtube.com/watch?v='
           + doc.xpath(r'//tr/@data-video-id')[0])
    time = doc.xpath(r'//div[@class="timestamp"]/span/text()')[0]
    title = doc.xpath(r'//tr/@data-title')[0]
    out = (url, time, title)
    return out

def print_data(data):
    """Print parts of data to the console."""
    print(*data)

def get_prog_args():
    """Parse command line arguments to a handy object with attributes."""
    desc = \
"""Load urls and information for videos in a video list on YouTube.

For the YouTube url with video list loads triples (url, time, title)
and prints them in format:

url time title\\n
url time title\\n
...

Example:

In:
ytlist https://www.youtube.com/playlist?list=ABCD

Out:
https://www.youtube.com/watch?v=123 1:01:01 Text of the title1
https://www.youtube.com/watch?v=456 2:02:02 Text of the title2
https://www.youtube.com/watch?v=789 3:03:03 Text of the title3

"""
    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('url', help='url to the videos list')
    parser.add_argument('--version', '-V',
                        action='version',
                        version='%(prog)s ' + 'v' + __version__)
    parser.add_argument('--license',
                        action='version',
                        version='License: ' + __license__ +
                        ', see more details at <http://www.gnu.org/licenses/>.',
                        help='show program\'s license and exit')
    return parser.parse_args()

def print_error(message):
    """Print an error message to stderr."""
    print('error:', message, file=sys.stderr)

def main():
    """Load urls and information for videos in a video list on YouTube."""
    args = get_prog_args()
    url = args.url
    page = load_page(url)
    for block in find_url_blocks(page):
        parsed_data = parse_block(block)
        print_data(parsed_data)
    return 0

if __name__ == '__main__':
    sys.exit(main())
