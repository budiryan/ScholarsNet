#for arxiv api
import urllib
import feedparser

#for database update
import json

base_url = 'http://export.arxiv.org/api/query?'
max_result = '100'
max_paper = '100'

queries = ['AR', 'AI', 'CL', 'CC', 'CE', 'CG', 'GT', 'CV', 'CY', 'CR', 'DS', 'DB',
         'DL', 'DM', 'DC', 'GL', 'GR', 'HC', 'IR', 'IT', 'LG', 'LO', 'MS', 'MA', 
         'MM', 'NI', 'NE', 'NA', 'OS', 'OH', 'PF', 'PL', 'RO', 'SE', 'SD', 'SC']

for query in queries:
    url = base_url + 'search_query=cat:cs.%s&start=0&max_results=%s' % (query, max_result)

#Search information such as total results
    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

#Run and parse query
    print 'Fetching paper'
    response = urllib.urlopen(url).read()
    print 'Parsing paper'
    feed = feedparser.parse(response)

#Read through all returned entries
    with open('data/db_arxiv_author_' + query + '.json', 'w') as f:
        f.write('[')
        for entry in feed.entries:

            authors = [a['name'] for a in entry.authors]
            print 'Authors: %s' % authors

            for author in authors:
                #Reformatting the name, eg 'B. R. Tija' becomes Tija_R
                name_tok = author.split(' ')
                print(name_tok)
                name = name_tok[-1] + ('_' + name_tok[-2][0] if len(name_tok) > 1 else '')

                #Formulate search on particular author
                #print '\nFetching authors'
                url2 = base_url + 'search_query=au:%s&start=0&max_results=%s' % (name, max_paper)
                try:
                    response2 = urllib.urlopen(url2).read()
                    #print 'Parsing authors'
                    feed2 = feedparser.parse(response2)

                    for entry2 in feed2.entries:

                        lead_author = author
                        arxiv_id = entry.id.split('/abs/')[-1].encode('utf-8')
                        published = entry.published.encode('utf-8')
                        title = entry.title.replace('\n', ' ').encode('utf-8')
                        other_authors = ', '.join(a.name if a.name != author else '' for a in entry2.authors)
                        category = entry.tags[0]['term'].encode('utf-8')
                        summary = entry.summary.encode('utf-8')

                        for l in entry.links:
                            if l.rel != 'alternate' and l.title == 'pdf':
                                link = l.href

                        #print 'arxiv-id: %s' % arxiv_id
                        #print 'Published: %s' % published
                        #print 'Title: %s' % title
                        #print 'Authors %s' % author
                        #print 'PDF link: %s' % link
                        #print 'Category: %s' % category
                        #print 'Summary: %s' % summary
                        #print '\n\n'

                        json.dump({'lead_author'    : lead_author,
                                   'arxiv-id'       : arxiv_id,
                                   'title'          : title,
                                   'other_authors'  : authors,
                                   'publish'        : published,
                                   'category'       : category,
                                   'link'           : link,
                                   'summary'        : summary},
                                   f, indent = 4)

                    f.write(',')
                except:
                    print 'url error'

        f.write('lol]')
            
    print 'Feed last updated %s' % feed.feed.updated
    print 'Total results: %s' % feed.feed.opensearch_totalresults
    print 'Items per page: %s' % feed.feed.opensearch_itemsperpage
