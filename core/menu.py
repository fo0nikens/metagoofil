#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
    This file is part of metagoofil
    Copyright (C) 2016 @maldevel
    https://github.com/maldevel/metagoofil
    
    metagoofil - extracting metadata of public documents
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    For more see the file 'LICENSE' for copying permission.
"""

__author__ = "maldevel"
__twitter__  = "@maldevel"
__version__ = "3.0"
__year__    = "2016"

from core.logger import Red
import argparse, os
from argparse import RawTextHelpFormatter

banner = """
{0} 

{1} Download public documents (pdf, doc, xls, ppt, etc..) available in the target websites.
{1} Copyright (c) {2} {3} ({4})

""".format(Red('metagoofil ' + __version__), Red('--['), __year__, __author__, __twitter__)

def csv_list(string):
    return string.split(',')  

parser = argparse.ArgumentParser(description=banner, formatter_class=RawTextHelpFormatter)

parser.add_argument('-d', dest='domain', action='store', help='Domain to search')
parser.add_argument('-t', dest='fileTypes', action='store', type=csv_list, help='Filetypes to download (pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx).  To search all 17,576 three-letter file extensions, type "ALL"')
parser.add_argument('-l', dest='searchMax', action='store', type=int, default=100, help='Maximum results to search (default 100)')
parser.add_argument('-n', dest='downloadFileLimit', action='store', type=int, default=100, help='Maximum number of files to download per filetype')
parser.add_argument('-m', dest='maxDownloadSize', action='store', type=int, default=5000000, help='Max filesize (in bytes) to download (default 5000000)')
parser.add_argument('-o', dest='saveDirectory', action='store', default=os.path.join(os.getcwd(), 'results'), help='Directory to save downloaded files (default is cwd, ".\results")')
parser.add_argument('-w', dest='downloadFiles', action='store_true', default=False, help='Download the files, instead of just viewing search results')
parser.add_argument('-f', dest='saveLinks', action='store_true', default=False, help='Save links to txt file')
parser.add_argument('-e', dest='delay', action='store', type=float, default=8.0, help='Delay (in seconds) between searches (default is 8).  If it\'s too small Google may block your IP, too big and your search may take a while.')
parser.add_argument('-i', dest='urlTimeout', action='store', type=int, default=30, help='Number of seconds to wait before timeout for unreachable/stale pages (default 30)')
parser.add_argument('-r', dest='numThreads', action='store', type=int, default=4, help='Number of search threads (default is 4)')
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Enable verbose output.')
parser.add_argument('--nolog', action='store_true', default=False, help='metagoofil will save a .log file. It is possible to tell metagoofil not to save those log files with this option.')

args = parser.parse_args()
