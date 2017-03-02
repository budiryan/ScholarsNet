#for arxiv api
import urllib
import feedparser

#for database update
import json

base_url = 'http://export.arxiv.org/api/query?'
max_result = '1000'

queries = ['AR', 'AI', 'CL', 'CC', 'CE', 'CG', 'GT', 'CV', 'CY', 'CR', 'DS', 'DB',
         'DL', 'DM', 'DC', 'GL', 'GR', 'HC', 'IR', 'IT', 'LG', 'LO', 'MS', 'MA', 
         'MM', 'NI', 'NE', 'NA', 'OS', 'OH', 'PF', 'PL', 'RO', 'SE', 'SD', 'SC']

for query in queries:
    url = base_url + 'search_query=cat:cs.%s&start=0&max_results=%s' % (query, max_result)

#Search information such as total results
    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

#Run and parse query
    response = urllib.urlopen(url).read()
    feed = feedparser.parse(response)

#Read through all returned entries
    with open('data/json/db_arxiv_' + query + '.json', 'w') as f:
        f.write('[')
        for entry in feed.entries:
            arxiv_id = entry.id.split('/abs/')[-1].encode('utf-8')
            published = entry.published.encode('utf-8')
            title = entry.title.replace('\n', ' ').encode('utf-8')
            author = entry.author.encode('utf-8')
            category = entry.tags[0]['term'].encode('utf-8')
            summary = entry.summary.encode('utf-8')

            for l in entry.links:
                if l.rel != 'alternate' and l.title == 'pdf':
                    link = l.href

            print 'arxiv-id: %s' % arxiv_id
            print 'Published: %s' % published
            print 'Title: %s' % title
            print 'Author %s' % author
            print 'PDF link: %s' % link
            print 'Category: %s' % category
            print 'Summary: %s' % summary
            print '\n\n'

            json.dump({'arxiv-id'   : arxiv_id,
                       'title'      : title,
                       'author'     : author,
                       'publish'    : published,
                       'category'   : category,
                       'link'       : link,
                       'summary'    : summary},
                       f, indent = 4)

            f.write(',')
        f.write('lol]')
            
    print 'Feed last updated %s' % feed.feed.updated
    print 'Total results: %s' % feed.feed.opensearch_totalresults
    print 'Items per page: %s' % feed.feed.opensearch_itemsperpage
