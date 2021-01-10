# -*- coding: utf-8 -*-
import scrapy, json, requests, sys, gzip, io, time, xlrd, pandas as pd
from scrapy.http import HtmlResponse

class CcrawlSpider(scrapy.Spider):
    name = 'ccrawl'
    allowed_domains = ['commoncrawl.org']

    def __init__(self, domain='', **kwargs):
        # Initializing all generic variables
        self.search_for_domain = domain
        self.get_idx_page_count = "http://index.commoncrawl.org/CC-MAIN-2020-45-index?url=*.{}/&showNumPages=true".format(self.search_for_domain)
        self.index_url = "http://index.commoncrawl.org/CC-MAIN-2020-45-index?url=*.{}&page={}&output=json"
        self.page_url = "https://commoncrawl.s3.amazonaws.com/{}"
        self.extraction_date = time.strftime("%Y-%m-%d")
        self.results = []
        super().__init__(**kwargs)


    # Function "start_requests": 
    #   Overides the Scrapy's start_url variable for custom URL inputs
    # Params: None
    # return: None
    def start_requests(self):
        # Small request to get number of pages indexed for a given domain
        print("\nFetching data for domain : {}\n".format(self.search_for_domain))
        page_num_resp = requests.get(self.get_idx_page_count)
        page_count_resp = json.loads(page_num_resp.text)
        total_idx_pages = int(page_count_resp['pages'])

        # Iterate over number of pages
        print("Found {} pages of indexed data for '{}'".format(total_idx_pages, self.search_for_domain))
        for i in range(total_idx_pages):
            idx_url = self.index_url.format(self.search_for_domain, i)
            print("[INFO] Fetching index data for page {} of {}".format((i+1), total_idx_pages))
            # Get the data from current page
            yield scrapy.Request(idx_url, meta={'idx_page_num':i}, callback=self.parse, dont_filter = True)

        # Creating backup output file when the crawling is completed
        # Creating a Pandas DataFrame from a list of dictionaries
        df = pd.DataFrame(self.results, columns=['URL','Title'])
        # removing duplicates from DataFrame
        out_df = df.drop_duplicates()

        # Pushing the DataFrame to .XLSX file
        out_df.to_excel("cnn.com-output-{}.xlsx".format(self.extraction_date), index=False)


    # Function "create_output": 
    #   Parse the indexed data from an index page and fetch the offset, length and WARC filename
    # Params: 
    #   1. response - scrapy Request's response
    # return: None
    def parse(self, response):
        if response.status == 200:
            idx_data = response.text.splitlines()
            print("Found {} items indexed in page : {}\n".format(len(idx_data), (response.meta['idx_page_num']+1)))

            # Iterate over number of indexed data per index page
            i = 1
            for itm in idx_data:
                print("getting data for item_no.: {} of {}".format(i, len(idx_data)))
                itm_data = json.loads(itm)
                print("Status code found : {}\n".format(itm_data['status']))

                # We'll move ahead if the status of the indexed data is in HTTP code 200's range.
                # Because there would be no title for other HTTP codes
                if '20' in itm_data['status']:
                    # Setting offset and limit of data to be fetched from WARC file
                    offset = int(itm_data['offset'])
                    limit_to = int(itm_data['offset']) + (int(itm_data['length']) - 1)
                    headers = {
                    'Range' : "bytes={}-{}".format(offset, limit_to)
                    }
                    url = self.page_url.format(itm_data['filename'])
                    # Fetching the required part of WARC file
                    # As full WARC file would contains other website data
                    # and would be very big in size.
                    yield scrapy.Request(url, headers=headers, meta={'itm_data':itm_data}, callback=self.get_page_data, dont_filter = True)
                i += 1


    # Function "create_output": 
    #   Parse the WARC file chunk and gather the required information
    # Params: 
    #   1. response - scrapy Request's response
    # return: None (only conditional blank returns)
    def get_page_data(self, response):
        try:
            # Try to extract WARC data from bytes
            raw_data = io.BytesIO(response.body)
            data_file = gzip.GzipFile(fileobj=raw_data)
            data = data_file.read().decode('utf-8')
        except:
            return

        cc_resp = ""

        if len(data) > 0:
            try:
                # Splitting the Metadata, Headers and actual webpage source from WARC chunk
                cc_meta, cc_header, cc_resp = data.strip().split('\r\n\r\n', 2)
            except:
                return

        if cc_resp != "":
            # Creating a dictionary of metadata on the fly from string
            mt = cc_meta.split('\r\n')
            mt[0] = '_:{}'.format(mt[0])
            meta = {j[0].strip():j[1].strip() for j in (i.split(":",1) for i in mt)}

            # Get URL from WARC metadata
            url = meta['WARC-Target-URI']
            xresp = HtmlResponse(url=url, body=cc_resp, encoding='utf-8')
            # Get title from the webpage source
            title = xresp.xpath("//title/text()").get()
            if title is None:
                title = ''
            else:
                title = title.replace('\n','').strip()

            # Print and yield the output
            print("Data added to final result : (URL:{}, Title:{})\n".format(url, title))
            final_data = {'URL':url, 'Title':title}
            self.results.append(final_data)
            yield final_data