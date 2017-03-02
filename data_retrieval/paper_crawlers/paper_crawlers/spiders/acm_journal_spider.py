import scrapy
import urllib.parse


class AcmJournalSpiderInformation(scrapy.Spider):
    # A spider for crawling ACM Digital Library journals
    name = "acm_journal_information"
    start_urls = ['http://dl.acm.org/pubs.cfm?']

    def parse(self, response):
        # Expected response: list of ACM Journals' URLs
        base_url = 'http://dl.acm.org'
        urls = response.xpath('/html/body/div/table/tr/td[2]/a/@href').extract()
        acronym = response.xpath('/html/body/div/table/tr/td[2]/strong/text()').extract()
        for index, url in enumerate(urls):
            # print(acronym[index], url)
            yield scrapy.Request(urllib.parse.urljoin(base_url, url), callback=lambda r, acronym=acronym: self.parse_get_request(r, acronym[index]))

    def parse_get_request(self, response, acronym):
        # Expected response: The journal's detail page, have to get publication archive
        # Sample response: http://dl.acm.org/pub.cfm?id=J774&CFID=904291701&CFTOKEN=88041768
        # print('Entered parse get request: ', response.url)
        url_id = urllib.parse.parse_qs(response.url.split('?')[-1])['id'][0]
        base_url = 'http://dl.acm.org'
        request_url = 'pub_about.cfm?id=' + url_id + '&acronym=' + acronym

        journal_category = response.xpath('body/div[1]/table/tr/td[2]/a/@title').extract_first()
        query_description = response.xpath('//*[@id="toShow1"]/text()').extract()
        journal_category_description = ''
        for string in query_description:
            journal_category_description += string
        journal_category_data = {
            'journal category': journal_category,
            'journal category_description': journal_category_description
        }
        yield scrapy.http.Request(urllib.parse.urljoin(base_url, request_url), callback=lambda r, category=journal_category_data: self.parse_each_journal(r, category))

    def parse_each_journal(self, response, category):
        # Expected response: A page with list of responses
        final_data = {}
        final_data.update(category)
        publication_years = response.xpath('/html/body/table/tr[2]/td[2]/table/tr/td/table/tr[1]/td[2]/text()').extract_first()
        publication_count = int(response.xpath('/html/body/table/tr[2]/td[2]/table/tr/td/table/tr[3]/td[2]/text()').extract_first().replace(',', ''))
        citation_count = int(response.xpath('/html/body/table/tr[2]/td[2]/table/tr/td/table/tr[5]/td[2]/text()').extract_first().replace(',', ''))
        available_for_download = int(response.xpath('/html/body/table/tr[2]/td[2]/table/tr/td/table/tr[7]/td[2]/text()').extract_first().replace(',', ''))
        total_downloads = int(response.xpath('/html/body/table/tr[2]/td[2]/table/tr/td/table/tr[13]/td[2]/text()').extract_first().replace(',', ''))
        article_1_download = response.xpath('//*[@id="toShowTop10"]/ol/li[1]/a/text()').extract_first()
        article_2_download = response.xpath('//*[@id="toShowTop10"]/ol/li[2]/a/text()').extract_first()
        article_3_download = response.xpath('//*[@id="toShowTop10"]/ol/li[3]/a/text()').extract_first()
        article_4_download = response.xpath('//*[@id="toShowTop10"]/ol/li[4]/a/text()').extract_first()
        article_5_download = response.xpath('//*[@id="toShowTop10"]/ol/li[5]/a/text()').extract_first()
        article_6_download = response.xpath('//*[@id="toShowTop10"]/ol/li[6]/a/text()').extract_first()
        article_7_download = response.xpath('//*[@id="toShowTop10"]/ol/li[7]/a/text()').extract_first()
        article_8_download = response.xpath('//*[@id="toShowTop10"]/ol/li[8]/a/text()').extract_first()
        article_9_download = response.xpath('//*[@id="toShowTop10"]/ol/li[9]/a/text()').extract_first()
        article_10_download = response.xpath('//*[@id="toShowTop10"]/ol/li[10]/a/text()').extract_first()
        final_data.update({
            "publication years": publication_years,
            "publication count": publication_count,
            "citation count": citation_count,
            "available for download": available_for_download,
            "total downloads": total_downloads,
            "first most downloaded article": article_1_download,
            "second most downloaded article": article_2_download,
            "third most downloaded article": article_3_download,
            "fourth most downloaded article": article_4_download,
            "fifth most downloaded article": article_5_download,
            "sixth most downloaded article": article_6_download,
            "seventh most downloaded article": article_7_download,
            "eight most downloaded article": article_8_download,
            "ninth most downloaded article": article_9_download,
            "tenth most downloaded article": article_10_download
        })
        yield final_data
