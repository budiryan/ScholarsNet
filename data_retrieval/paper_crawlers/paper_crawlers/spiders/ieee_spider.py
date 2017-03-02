import scrapy
import json
import urllib.parse
import re
from scrapy import http
from scrapy_splash import SplashRequest


class IeeeSpider(scrapy.Spider):
    name = "ieee"

    def start_requests(self):
        url = 'http://ieeexplore.ieee.org/rest/publication'
        header = {'Accept': 'application/json, text/plain, */*',
                  'Content-Type': 'application/json;charset=UTF-8'}
        body = {"contentType": "conferences",
                "tabId": "topic",
                "publisher": "",
                "collection": "",
                "pageNumber": 1,
                "selectedValue": "4291946551"}
        yield http.Request(url, method="POST", body=json.dumps(body),
                           headers=header, callback=self.parse)

    def parse(self, response):
        total_page_number = 177
        url = 'http://ieeexplore.ieee.org/rest/publication'
        page_number = 1
        header = {'Accept': 'application/json, text/plain, */*',
                  'Content-Type': 'application/json;charset=UTF-8'}
        body = {"contentType": "conferences",
                "tabId": "topic",
                "publisher": "",
                "collection": "",
                "pageNumber": str(page_number),
                "selectedValue": "4291946551"}

        for i in range(total_page_number):
            yield http.Request(url, method="POST", body=json.dumps(body), headers=header,
                               callback=self.parse_records,
                               dont_filter=True)
            page_number += 1
            body["pageNumber"] = str(page_number)

    def parse_records(self, response):
        host = "http://ieeexplore.ieee.org"
        list_of_records = json.loads(response.body_as_unicode())["records"]

        # Each record has a list of titleHistory
        for record in list_of_records:
            if "titleHistory" in record:
                list_of_events = record["titleHistory"]
                for event in list_of_events:
                    # print("Link: ", urllib.parse.urljoin(
                    #     host, event["publicationLink"]))
                    yield scrapy.Request(urllib.parse.urljoin(host, event["publicationLink"]),
                                         callback=self.parse_papers)

    def parse_papers(self, response):
        # Response will be: A page with a list of research paper.
        # Request will be the links of individidual paper sites
        host = "http://ieeexplore.ieee.org"
        papers = response.xpath("//ul[contains(@class, 'results')]/li/div[contains(@class,'txt')]/h3/a/@href").extract()
        for paper in papers:
            link = urllib.parse.urljoin(host, paper)
            yield SplashRequest(link, self.parse_each_paper,
                                endpoint='render.html',
                                )

    def parse_each_paper(self, response):
        # Response would be individual page of each paper
        # Target: scrape the page and save to json / db
        id_number = re.search(r'[0-9]+', response.url).group(0)
        title = response.xpath('//*[@id="LayoutWrapper"]/div[6]/div[3]/div/section[1]/div[2]/div[1]/div[1]/h1/span/text()').extract_first()
        authors = response.xpath('//*[@id="LayoutWrapper"]/div[6]/div[3]/div/div/div/div[2]/div/div/span/span/a/span/text()').extract()
        abstract = response.xpath('//*[@id="' + str(id_number) + '"]/div[1]/div/div/div/text()').extract_first()
        published_in = response.xpath('//*[@id="' + str(id_number) + '"]/div[2]/a/text()').extract_first()
        try:
            date_of_conference = response.xpath('//*[@id="' + str(id_number) + '"]/div[3]/div[1]/div[1]/text()').extract()[-1].strip()
        except:
            date_of_conference = None
        try:
            electronic_isbn = response.xpath('//*[@id="' + str(id_number) + '"]/div[3]/div[1]/div[3]/div[2]/div[1]/text()').extract()[-1].strip()
        except:
            electronic_isbn = None
        try:
            print_on_demand_isbn = response.xpath('//*[@id="' + str(id_number) + '"]/div[3]/div[1]/div[3]/div[2]/div[2]/text()').extract()[-1].strip()
        except:
            print_on_demand_isbn = None
        pdf_link = urllib.parse.urljoin("http://ieeexplore.ieee.org", response.url)
        yield {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "published in": published_in,
            "Date of Conference": date_of_conference,
            "Electronic ISBN": electronic_isbn,
            "Print on Demand ISBN": print_on_demand_isbn,
            "PDF Link": pdf_link
        }
