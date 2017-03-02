import scrapy
import json
import urllib.parse
import re
from scrapy import http
from scrapy_splash import SplashRequest


class IeeeSpider(scrapy.Spider):
    name = "ieee_journal"

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

        

    # def parse_records(self, response):
    #     host = "http://ieeexplore.ieee.org"
    #     list_of_records = json.loads(response.body_as_unicode())["records"]

    #     # Each record has a list of titleHistory
    #     for record in list_of_records:
    #         if "titleHistory" in record:
    #             list_of_events = record["titleHistory"]
    #             for event in list_of_events:
    #                 yield scrapy.Request(urllib.parse.urljoin(host, event["publicationLink"]),
    #                                      callback=self.parse_papers)

    # def parse_papers(self, response):
    #     # Response will be: A page with a list of research paper.
    #     # Request will be the links of individidual paper sites
    #     host = "http://ieeexplore.ieee.org"
    #     papers = response.xpath("//ul[contains(@class, 'results')]/li/div[contains(@class,'txt')]/h3/a/@href").extract()
    #     for paper in papers:
    #         link = urllib.parse.urljoin(host, paper)
    #         yield SplashRequest(link, self.parse_each_paper,
    #                             endpoint='render.html',
    #                             )
