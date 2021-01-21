# common_crawl_with_scrapy
Parsing Common Crawl data with Python and Scrapy.

## What is Common Crawl
Common Crawl is a nonprofit 501 organization that crawls the web and freely provides its archives and datasets to the public. Common Crawl's web archive consists of petabytes of data collected since 2011. It completes crawls generally every month.

## Types of files available on Common Crawl
Common Crawl currently stores the crawl data using the Web ARChive (WARC) format.
Before that point, the crawl was stored in the ARC file format.
The WARC format allows for more efficient storage and processing of Common Crawl’s free multi-billion page web archives, which can be hundreds of terabytes in size.
This document aims to give you an introduction to working with the new format, specifically the difference between:

1. WARC files which store the raw crawl data
2. WAT files which store computed metadata for the data stored in the WARC
3. WET files which store extracted plaintext from the data stored in the WARC

## Things done in this repo
I have parsed the WARC files of Oct 2020 to gather URLs and Titles of all pages for a given domain. This can be changed according to the use case.
