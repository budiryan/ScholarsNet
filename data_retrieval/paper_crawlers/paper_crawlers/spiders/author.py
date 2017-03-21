import scrapy
import urllib.parse
import re

recorded_authors = []


class AuthorSpider(scrapy.Spider):
    # A spider for crawling ACM Digital Library journals
    name = "author"
    start_urls = ['http://dl.acm.org/pubs.cfm?']
    custom_setting = {
        'LOG_LEVEL': 'DEBUG',
        'ROBOTSTXT_OBEY': True,
        'COOKIES_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0 Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'
    }

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
        # print(urllib.parse.urljoin(base_url, request_url))
        yield scrapy.http.Request(urllib.parse.urljoin(base_url, request_url), callback=lambda r, parent_url=response.url: self.parse_each_journal(r, parent_url))

    def parse_each_journal(self, response, parent_url):
        # Expected response: A page with list of responses
        base_url = 'http://dl.acm.org'
        # print('Entered parsed each journal')
        urls = response.xpath('/html/body/div/table/tr/td[1]/a/@href').extract()
        for url in urls:
            url = url.split('&')[0]
            yield scrapy.Request(urllib.parse.urljoin(base_url, url), callback=lambda r, parent_url=parent_url: self.parse_get_request2(r, parent_url))

    def parse_get_request2(self, response, parent_url):
        # Expected response: The volume's detail page, have to get table of contents consisting each paper
        # Example request: http://dl.acm.org/tab_about.cfm?id=3022634&type=issue&parent_id=J204
        # Required fields: response id, type=issue, parent_id
        base_url = 'http://dl.acm.org'
        parent_id = urllib.parse.parse_qs(parent_url.split('?')[-1])['id'][0]
        url_id = urllib.parse.parse_qs(response.url.split('?')[-1])['id'][0]
        request = '/tab_about.cfm?id=' + url_id + '&type=issue&parent_id=' + parent_id
        yield scrapy.http.Request(urllib.parse.urljoin(base_url, request), callback=self.parse_paper)

    def parse_paper(self, response):
        # Expected response: A page with a list of research papers
        base_url = 'http://dl.acm.org'
        link_list = response.xpath('/html/body/div/table/tr/td[2]/span/a/@href').extract()
        authors_link = [link.split('&')[0] for link in link_list if re.search(r'author_page+', link) is not None]
        for link in authors_link:
            yield scrapy.http.Request(urllib.parse.urljoin(base_url, link), callback=self.parse_each_author)

    def parse_each_author(self, response):
        base_url = 'http://dl.acm.org'
        name = response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[1]/table/tr/td[2]/span[1]/strong/text()').extract_first()
        website = response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[1]/table/tr/td[2]/span[2]/a/@href').extract_first()
        email_list = response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[1]/table/tr/td[2]/div/text()').extract()
        if email_list:
            email = email_list[0] + '@' + email_list[-1]
        else:
            email = None
        image = urllib.parse.urljoin(base_url, response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[1]/table/tr/td[1]/div/img/@src').extract_first())
        affiliation = response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[2]/table/tr/td/div/a/text()').extract()
        try:
            citation_count = int(re.sub(',', '', response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[3]/table/tr/td/table/tr[3]/td[2]/text()').extract_first()))
        except TypeError:
            citation_count = 0
        try:
            publication_count = int(re.sub(',', '', response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[3]/table/tr/td/table/tr[5]/td[2]/text()').extract_first()))
        except TypeError:
            publication_count = 0
        try:
            publication_years = response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[3]/table/tr/td/table/tr[7]/td[2]/text()').extract_first()
        except TypeError:
            publication_years = "Unknown"
        try:
            total_downloads = int(re.sub(',', '', response.xpath('/html/body/div[1]/table/tr[2]/td/table/tr[1]/td[3]/table/tr/td/table/tr[13]/td[2]/text()').extract_first()))
        except TypeError:
            total_downloads = 0

        yield{
            'name': name,
            'website': website,
            'email': email,
            'photo': image,
            'university': affiliation,
            'citation count': citation_count,
            'publication count': publication_count,
            'publication years': publication_years,
            'total downloads': total_downloads
        }
