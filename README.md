# metagoofil

**Download public documents (pdf, doc, xls, ppt, etc..) available in the target websites.**


**Requirements**
---
Python 2.x


**Older versions**
---
Previous version of metagoofil written by @opsdisk.
https://github.com/opsdisk/metagoofil


Original version of metagoofil written by Christian Martorella [@laramies]
https://github.com/laramies/metagoofil

**Usage**
---
```
usage: metagoofil.py [-h] [-d DOMAIN] [-t FILETYPES] [-l SEARCHMAX]
                     [-n DOWNLOADFILELIMIT] [-m MAXDOWNLOADSIZE]
                     [-o SAVEDIRECTORY] [-w] [-f] [-e DELAY] [-i URLTIMEOUT]
                     [-r NUMTHREADS] [-v] [--nolog]

metagoofil 3.0.1

--[ Download public documents (pdf, doc, xls, ppt, etc..) available in the target websites.
--[ Copyright (c) 2016 maldevel (@maldevel)

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN             Domain to search
  -t FILETYPES          Filetypes to download (pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx).  To search all 17,576 three-lett
er file extensions, type "ALL"
  -l SEARCHMAX          Maximum results to search (default 100)
  -n DOWNLOADFILELIMIT  Maximum number of files to download per filetype
  -m MAXDOWNLOADSIZE    Max filesize (in bytes) to download (default 5000000)
  -o SAVEDIRECTORY      Directory to save downloaded files (default is cwd, ".
                        esults")
  -w                    Download the files, instead of just viewing search results
  -f                    Save links to txt file
  -e DELAY              Delay (in seconds) between searches (default is 8).  If it's too small Google may block your IP,
 too big and your search may take a while.
  -i URLTIMEOUT         Number of seconds to wait before timeout for unreachable/stale pages (default 30)
  -r NUMTHREADS         Number of search threads (default is 4)
  -v, --verbose         Enable verbose output.
  --nolog               metagoofil will save a .log file. It is possible to tell metagoofil not to save those log files
with this option.
```

