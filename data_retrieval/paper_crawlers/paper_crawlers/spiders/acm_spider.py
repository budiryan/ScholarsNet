import scrapy
import urllib.parse
import re


class AcmJournalSpider(scrapy.Spider):
    # A spider for crawling ACM Digital Library journals
    name = "acm_journal"
    start_urls = ['http://dl.acm.org/pubs.cfm?']

    def parse(self, response):
        # Expected response: list of ACM Journals' URLs
        base_url = 'http://dl.acm.org'
        urls = response.xpath('/html/body/div/table/tr/td[2]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(urllib.parse.urljoin(base_url, url), callback=self.parse_get_request)

    def parse_get_request(self, response):
        # Expected response: The journal's detail page, have to get publication archive
        # Sample response: http://dl.acm.org/pub.cfm?id=J774&CFID=904291701&CFTOKEN=88041768
        # print('Entered parse get request: ', response.url)
        url_id = urllib.parse.parse_qs(response.url.split('?')[-1])['id'][0]
        base_url = 'http://dl.acm.org'
        request_url = 'pub_series.cfm?id=' + url_id + '&_cf_containerId=pubs&_cf_nodebug=true&_cf_nocache=true&_cf_rc=1'
        journal_category = response.xpath('body/div[1]/table/tr/td[2]/a/@title').extract_first()
        query_description = response.xpath('//*[@id="toShow1"]/text()').extract()
        journal_category_description = ''
        for string in query_description:
            journal_category_description += string
        journal_category_data = {
            'journal category': journal_category,
            'journal category_description': journal_category_description
        }
        # print(urllib.parse.urljoin(base_url, request_url))
        yield scrapy.http.Request(urllib.parse.urljoin(base_url, request_url), callback=lambda r, parent_url=response.url,
                                  category=journal_category_data: self.parse_each_journal(r, parent_url, category))

    def parse_each_journal(self, response, parent_url, category):
        # Expected response: A page with list of responses
        base_url = 'http://dl.acm.org'
        # print('Entered parsed each journal')
        urls = response.xpath('/html/body/div/table/tr/td[1]/a/@href').extract()
        for url in urls:
            url = url.split('&')[0]
            yield scrapy.Request(urllib.parse.urljoin(base_url, url),
                                 callback=lambda r, parent_url=parent_url, category=category: self.parse_get_request2(r, parent_url, category))

    def parse_get_request2(self, response, parent_url, category):
        # Expected response: The volume's detail page, have to get table of contents consisting each paper
        # Example request: http://dl.acm.org/tab_about.cfm?id=3022634&type=issue&parent_id=J204
        # Required fields: response id, type=issue, parent_id
        base_url = 'http://dl.acm.org'
        parent_id = urllib.parse.parse_qs(parent_url.split('?')[-1])['id'][0]
        url_id = urllib.parse.parse_qs(response.url.split('?')[-1])['id'][0]
        request = '/tab_about.cfm?id=' + url_id + '&type=issue&parent_id=' + parent_id
        volume_and_time = response.xpath('//*[@id="divmain"]/div/text()').extract()[1].strip()
        category.update({
            'volume': volume_and_time.split(',')[0].strip(),
            'time added': volume_and_time.split(',')[1].strip()
        })
        yield scrapy.http.Request(urllib.parse.urljoin(base_url, request), callback=lambda r, category=category: self.parse_paper(r, category))

    def parse_paper(self, response, category):
        # Expected response: A page with a list of research papers
        base_url = 'http://dl.acm.org'
        link_list = response.xpath('/html/body/div/table/tr/td[2]/span/a/@href').extract()
        paper_url_list = [url.split('&')[0] for url in link_list if re.search(r'citation', url) is not None]
        for url in paper_url_list:
            # print('url is: ', url)
            yield scrapy.Request(urllib.parse.urljoin(base_url, url), callback=lambda r, category=category: self.parse_each_paper(r, category))

    def parse_each_paper(self, response, category):
        # Expected response: A detail page of each research paper, this is the final stage of crawling
        # Sample response URL: http://dl.acm.org/tab_abstract.cfm?id=2964909
        base_url = 'http://dl.acm.org'
        # print('Respons URL is: ', response.url)
        url_id = urllib.parse.parse_qs(response.url.split('?')[-1])['id'][0]
        link_list = response.xpath('//a/text()').extract()
        doi = None
        for link in link_list:
            if re.search(r'[0-9]+', link):
                doi = link

        # QUIT IF THERE IS NO DOI AT ALL! UM, GONNA TEST FIRST
        if doi is None:
            yield

        request_url = 'tab_abstract.cfm?id=' + url_id
        # Fields: title, authors, abstract, citation count, published_in, download_count, pdf_link
        title = response.xpath('//*[@id="divmain"]/div/h1/strong/text()').extract_first()
        # if doi == None:
        #     doi = response.xpath('//*[@id="divmain"]/table[2]/tr/td/table/tr[4]/td/span[3]/a/text()').extract_first()
        author = response.xpath('//*[@id="divmain"]/table/tr/td[1]/table[2]/tr/td[2]/a/text()').extract_first()
        other_authors = response.xpath('//*[@id="divmain"]/table/tr/td[1]/table[2]/tr/td[2]/a/text()').extract()[1:]
        citation_count = int(response.xpath('//*[@id="divmain"]/table/tr/td[2]/table/tr[3]/td/text()[1]').extract_first().strip().split(':')[-1].strip().replace(',', ''))
        download_count = int(response.xpath('//*[@id="divmain"]/table/tr/td[2]/table/tr[3]/td/text()[2]').extract_first().strip().split(':')[-1].strip().replace(',', ''))
        pdf_link = urllib.parse.urljoin(base_url, response.xpath('//*[@id="divmain"]/table/tr/td[1]/table[1]/tr/td[2]/a/@href').extract_first())
        data = {
            'title': title,
            'doi': doi,
            'citation count': citation_count,
            'download count': download_count,
            'pdf link': pdf_link,
            'author': author,
            'other_authors': other_authors
        }
        data.update(category)
        yield scrapy.Request(urllib.parse.urljoin(base_url, request_url), callback=lambda r, data=data: self.parse_paper_abstract(r, data))

    def parse_paper_abstract(self, response, data):
        # Still have to make one more call just to get the paper's abstract, OH MY GOD
        # Sample response URL: http://dl.acm.org/tab_abstract.cfm?id=2964909
        abstract_query = response.xpath('/html/body/div/div/p/text()').extract()
        if len(abstract_query) == 0:
            data['abstract'] = ''
        else:
            final_abstract = ''
            for a in abstract_query:
                final_abstract += a
            data['abstract'] = final_abstract
        yield data
