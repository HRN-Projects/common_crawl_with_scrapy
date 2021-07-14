# common_crawl_with_scrapy
Parsing Huge Web Archive files from Common Crawl data index to fetch any required domain's data concurrently with Python and Scrapy.

## About Common Crawl and this repository -
### What is Common Crawl
Common Crawl is a nonprofit 501 organization that crawls the web and freely provides its archives and datasets to the public. Common Crawl's web archive consists of petabytes of data collected since 2011. It completes crawls generally every month.

### Types of files available on Common Crawl
Common Crawl currently stores the crawl data using the Web ARChive (WARC) format.
Before that point, the crawl was stored in the ARC file format.
The WARC format allows for more efficient storage and processing of Common Crawl’s free multi-billion page web archives, which can be hundreds of terabytes in size.

Below are the different types of files available on Common Crawl:

* WARC files which store the raw crawl data
* WAT files which store computed metadata for the data stored in the WARC
* WET files which store extracted plaintext from the data stored in the WARC

### Things done in this repo
I have parsed the WARC files of Oct 2020 to gather URLs and Titles of all pages for a given domain. This can be changed according to the use case.


## How to use -
Code can be executed in two ways -
### Enter scrapy crawl command on terminal :
1. Go to "scrapy_code\ccFetch\."
2. Open CMD or terminal
3. Type command -
`scrapy crawl ccrawl -o filename.csv -a domain=your_domain.com`

### Use the python script :
1. Go to "scrapy_code\ccFetch\."
2. Open CMD or terminal
3. Type command -
`python run_prog.py`
4. Enter the values for required argurments and the code execution will start.
    
Note :
1. "-o" was used for passing output file name to crawler.
2. "-a" was used to pass any expected argument (e.g. - domain, in this case).
    
