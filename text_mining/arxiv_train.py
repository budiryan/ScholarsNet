#!/usr/bin/env python

#for arxiv api
import urllib.request, urllib.parse, urllib.error
import feedparser

#for database update
import json

base_url = 'http://export.arxiv.org/api/query?'
max_result = '10000'

queries = ['AR', 'AI', 'CL', 'CC', 'CE', 'CG', 'GT', 'CV', 'CY', 'CR', 'DS', 'DB',
         'DL', 'DM', 'DC', 'GL', 'GR', 'HC', 'IR', 'IT', 'LG', 'LO', 'MS', 'MA', 
         'MM', 'NI', 'NE', 'NA', 'OS', 'OH', 'PF', 'PL', 'RO', 'SE', 'SD', 'SC']

for query in queries:
    url = base_url + 'search_query=cat:cs.%s&start=0&max_results=%s' % (query, max_result)

#Search information such as total results
    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

#Run and parse query
    response = urllib.request.urlopen(url).read()
    feed = feedparser.parse(response)

#Read through all returned entries
    with open('json/db_arxiv_' + query + '.json', 'w') as f:
        f.write('[')
        for entry in feed.entries:
            arxiv_id = entry.id.split('/abs/')[-1].encode('utf-8')
            published = entry.published.encode('utf-8')
            title = entry.title.replace('\n', ' ').encode('utf-8')
            author = entry.author.encode('utf-8')
            other_authors = ', '.join(a.name for a in entry.authors if a != author)
            category = entry.tags[0]['term'].encode('utf-8')
            summary = entry.summary.encode('utf-8')

            for l in entry.links:
                if l.rel == 'alternate':
                    pass
                elif l.title == 'pdf':
                    link = l.href
                elif l.title == 'doi':
                    doi = l.href.split(".org/", 1)[1]

            print('Title: %s' % title)
            print('Category: %s' % category)
            print('Summary: %s' % summary)
            print('\n\n')

            json.dump({'title'   : title,
                       'category': category,
                       'summary' : summary},
                       f, indent = 4)

            f.write(',')
        f.write('lol]')
            
    print('Feed last updated %s' % feed.feed.updated)
    print('Total results: %s' % feed.feed.opensearch_totalresults)
    print('Items per page: %s' % feed.feed.opensearch_itemsperpage)
