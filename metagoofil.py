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

__author__ = "maldevel, opsdisk.com and Christian Martorella"
__copyright__ = "Copyright (c) 2016 @maldevel"
__credits__ = ["maldevel", "opsdisk.com", "Christian Martorella"]
__license__ = "GPLv3"
__version__ = "3.0"
__maintainer__ = "maldevel"


from __future__ import print_function

import argparse, google, os, Queue, sys
import threading, time, urllib, urllib2


class BackgroundWorker(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while True:          
            # Grab URL off the queue
            url = mg.queue.get()
            try:
                response = urllib2.urlopen(url, timeout=5)
                # Determine if file is small enough to download
                size = int(response.headers["Content-Length"])
                if (size > mg.maxDownloadSize):
                    print("[-] File is too large [" + str(size) + " bytes] to download " + url)
                else:
                    print("[+] Downloading file - [" + str(size) + " bytes] " + url)
                    filename = str(url.split("/")[-1]) 
                    urllib.urlretrieve(url, mg.saveDirectory + "/" + filename)
                    mg.totalBytes += size
                    
            except:
                print("[-] Timed out after " + str(mg.urlTimeout) + " seconds...can't reach url: " + url)
            
            mg.queue.task_done()


class Metagoofil:

    def __init__(self, domain, fileTypes, searchMax, downloadFileLimit, maxDownloadSize, saveDirectory, downloadFiles, saveLinks, delay, urlTimeout, numThreads):
        self.domain = domain
        self.fileTypes = fileTypes
        self.searchMax = searchMax
        self.downloadFileLimit = downloadFileLimit
        self.maxDownloadSize = maxDownloadSize
        self.saveDirectory = saveDirectory
        self.downloadFiles = downloadFiles
        self.saveLinks = saveLinks
        self.delay = delay
        self.totalBytes = 0
        self.urlTimeout = urlTimeout
        
        # Create queue and specify the number of worker threads.
        self.queue = Queue.Queue() 
        self.numThreads = numThreads

        

    def go(self):
        # Kickoff the threadpool.
        for i in range(self.numThreads):
            thread = BackgroundWorker()
            thread.daemon = True
            thread.start()

        if "ALL" in self.fileTypes:
            from itertools import product
            from string import ascii_lowercase
            # Generate all three letter combinations
            self.fileTypes = [''.join(i) for i in product(ascii_lowercase, repeat=3)]

        for filetype in self.fileTypes:
            self.files = []  # Stores URLs with files, clear out for each filetype

            # Search for the files to download
            print("[*] Searching for " + str(self.searchMax) + " ." + filetype + " files and waiting " + str(self.delay) + " seconds between searches")
            query = "filetype:" + filetype + " site:" + self.domain
            for url in google.search(query, start=0, stop=self.searchMax, num=100, pause=self.delay):
                self.files.append(url)
            
            # Since google.search method retreives URLs in batches of 100, ensure the file list only contains the requested amount
            if len(self.files) > self.searchMax:
                self.files = self.files[:-(len(self.files) - self.searchMax)] 
                        
            # Download files if specified with -w switch
            if self.downloadFiles:
                self.download()
            
            # Otherwise, just display them
            else:
                print("[*] Results: " + str(len(self.files)) + " ." + filetype + " files found")
                for f in self.files:
                    print(f)
            
            # Save links to output to file
            if self.saveLinks:
                self.f = open('html_links_' + get_timestamp() + '.txt', 'a')
                for f in self.files:
                    self.f.write(f + "\n")
                self.f.close()
        
        if self.downloadFiles:
            print("[+] Total download: " + str(self.totalBytes) + " bytes / " + str(self.totalBytes / 1024) + " KB / " + str(self.totalBytes / (1024 * 1024)) + " MB")
                      
    def download(self):
        self.counter = 1
        for url in self.files:
            if self.counter <= self.downloadFileLimit:
                self.queue.put(url)
                self.counter += 1

        self.queue.join()


def get_timestamp():
    now = time.localtime()
    timestamp = time.strftime('%Y%m%d_%H%M%S', now)
    return timestamp


def csv_list(string):
    return string.split(',')                    

 
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Metagoofil - Search and Download Filetypes')
    parser.add_argument('-d', dest='domain', action='store', required=True, help='Domain to search')
    parser.add_argument('-t', dest='fileTypes', action='store', required=True, type=csv_list, help='Filetypes to download (pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx).  To search all 17,576 three-letter file extensions, type "ALL"')
    parser.add_argument('-l', dest='searchMax', action='store', type=int, default=100, help='Maximum results to search (default 100)')
    parser.add_argument('-n', dest='downloadFileLimit', action='store', type=int, help='Maximum number of files to download per filetype')
    parser.add_argument('-m', dest='maxDownloadSize', action='store', type=int, default=5000000, help='Max filesize (in bytes) to download (default 5000000)')
    parser.add_argument('-o', dest='saveDirectory', action='store', default=os.getcwd(), help='Directory to save downloaded files (default is cwd, ".")')
    parser.add_argument('-w', dest='downloadFiles', action='store_true', default=False, help='Download the files, instead of just viewing search results')
    parser.add_argument('-f', dest='saveLinks', action='store_true', default=False, help='Save the html links to html_links_<TIMESTAMP>.txt file')
    parser.add_argument('-e', dest='delay', action='store', type=float, default=7.0, help='Delay (in seconds) between searches.  If it\'s too small Google may block your IP, too big and your search may take a while.')
    parser.add_argument('-i', dest='urlTimeout', action='store', type=int, default=5, help='Number of seconds to wait before timeout for unreachable/stale pages (default 5)')
    parser.add_argument('-r', dest='numThreads', action='store', type=int, default=8, help='Number of search threads (default is 8)')

    args = parser.parse_args()

    if not args.domain:
        print("[!] Specify a domain with -d")
        sys.exit()
    if not args.fileTypes:
        print("[!] Specify file types with -t")
        sys.exit()
    if (args.downloadFileLimit > 0) and (args.downloadFiles is False):
        print("[+] Adding -w for you")
        args.downloadFiles = True
    if args.saveDirectory:
        print("[*] Downloaded files will be saved here: " + args.saveDirectory)
        if not os.path.exists(args.saveDirectory):
            print("[+] Creating folder: " + args.saveDirectory)
            os.mkdir(args.saveDirectory)
    if args.delay < 0:
        print("[!] Delay must be greater than 0")
        sys.exit()
    if args.urlTimeout < 0:
        print("[!] URL timeout (-i) must be greater than 0")
        sys.exit()
    if args.numThreads < 0:
        print("[!] Number of threads (-n) must be greater than 0")
        sys.exit()

    #print vars(args)
    mg = Metagoofil(**vars(args))
    mg.go()

    print("[+] Done!")
