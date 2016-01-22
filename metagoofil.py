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

from __future__ import print_function

__author__ = "maldevel, opsdisk.com and Christian Martorella"
__copyright__ = "Copyright (c) 2016 @maldevel"
__credits__ = ["maldevel", "opsdisk.com", "Christian Martorella"]
__license__ = "GPLv3"
__version__ = "3.0"
__maintainer__ = "maldevel"


import os, sys
from core.menu import args,banner
from core.harvester import Metagoofil
from core.logger import Logger
 
if __name__ == "__main__":
    
    logsDir = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(logsDir):
        os.mkdir(logsDir)
        
    logger = Logger(args.nolog, args.verbose)
        
    if not args.domain:
        logger.PrintError("Specify a domain with -d")
        sys.exit()
    if not args.fileTypes:
        logger.PrintError("Specify file types with -t")
        sys.exit()
    if (args.downloadFileLimit > 0) and (args.downloadFiles is False):
        logger.Print("Adding -w for you")
        args.downloadFiles = True
    if args.saveDirectory:
        logger.Print("Downloaded files will be saved here: " + args.saveDirectory)
        if not os.path.exists(args.saveDirectory):
            logger.Print("Creating folder: " + args.saveDirectory)
            os.mkdir(args.saveDirectory)
    if args.delay < 0:
        logger.PrintError("Delay must be greater than 0")
        sys.exit()
    if args.urlTimeout < 0:
        logger.PrintError("URL timeout (-i) must be greater than 0")
        sys.exit()
    if args.numThreads < 0:
        logger.PrintError("Number of threads (-n) must be greater than 0")
        sys.exit()

    print(banner)
    
    #print vars(args)
    mg = Metagoofil(**vars(args))
    mg.go()

    logger.Print("Done!")
