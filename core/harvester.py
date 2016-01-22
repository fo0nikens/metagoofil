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

import google, Queue, os
import threading, time, urllib, urllib2
from core.logger import Logger

class BackgroundWorker(threading.Thread):

    def __init__(self, mg, logger):
        threading.Thread.__init__(self)
        self.mg = mg
        self.logger = logger 
        
    def run(self):
        while True:          
            # Grab URL off the queue
            url = self.mg.queue.get()
            try:
                response = urllib2.urlopen(url, timeout=5)
                # Determine if file is small enough to download
                size = int(response.headers["Content-Length"])
                if (size > self.mg.maxDownloadSize):
                    self.logger.PrintError("File is too large [" + str(size) + " bytes] to download " + url)
                else:
                    self.logger.Print("Downloading file - [" + str(size) + " bytes] " + url)
                    filename = str(url.split("/")[-1]) 
                    urllib.urlretrieve(url, self.mg.saveDirectory + "/" + filename)
                    self.mg.totalBytes += size
                    
            except:
                self.logger.PrintError("Timed out after " + str(self.mg.urlTimeout) + " seconds...can't reach url: " + url)
            
            self.mg.queue.task_done()


class Metagoofil:

    def __init__(self, domain, fileTypes, searchMax, downloadFileLimit, 
                 maxDownloadSize, saveDirectory, downloadFiles, saveLinks, 
                 delay, urlTimeout, numThreads, verbose, nolog):
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
        self.logger = Logger(nolog, verbose)
        
        # Create queue and specify the number of worker threads.
        self.queue = Queue.Queue() 
        self.numThreads = numThreads

    def go(self):
        # Kickoff the threadpool.
        for i in range(self.numThreads):
            thread = BackgroundWorker(self, self.logger)
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
            self.logger.Print("Searching for " + str(self.searchMax) + " ." + filetype + " files and waiting " + str(self.delay) + " seconds between searches")
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
                self.logger.Print("Results: " + str(len(self.files)) + " ." + filetype + " files found")
                for f in self.files:
                    print(f)
            
            # Save links to output to file
            if self.saveLinks:
                self.f = open(os.path.join(os.getcwd(), 'results', 'html_links_' + self.get_timestamp() + '_' + self.domain + '.txt'), 'a')
                for f in self.files:
                    self.f.write(f + "\n")
                self.f.close()
        
        if self.downloadFiles:
            self.logger.Print("Total download: " + str(self.totalBytes) + " bytes / " + str(self.totalBytes / 1024) + " KB / " + str(self.totalBytes / (1024 * 1024)) + " MB")
                      
    def download(self):
        self.counter = 1
        for url in self.files:
            if self.counter <= self.downloadFileLimit:
                self.queue.put(url)
                self.counter += 1

        self.queue.join()

    def get_timestamp(self):
        now = time.localtime()
        timestamp = time.strftime('%Y%m%d_%H%M%S', now)
        return timestamp
    