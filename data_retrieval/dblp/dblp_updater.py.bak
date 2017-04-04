from html.parser import HTMLParser
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

#Main html fetch class
class MyHTMLParser(HTMLParser):
    
    check = False
    content = False
    data = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.check = True 
        elif self.content and tag == 'h3':
            self.content = False
            print(self.data + '\n')

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.check and (data == 'Abstract' or data == 'Summary'):
            self.check = False
            self.content = True
        elif self.content:
            self.data += data

    def get_data(self):
        data = self.data
        self.data = ''
        return data

print('Parsing XML')

#Load xml file
tree = ET.parse('trim_dblp.xml')
root = tree.getroot()

print('Parse complete')
print('Fetching url')

#Excluding phd thesis etc
for i in range(len(root)):
    if root[i].tag != 'article':
        break

#Limiting the max number of entries to be 10000
print('Number of articles: ', i)
i = min(i, 1460)
print('Number of articles after trimming: ', i)
root = root[:i]

#For indexing
i = 0
#Fetch summary/abstract from each entry
for child in root:
    
    if child.tag == 'article':
        i += 1
        for c in child[0:]:
            if c.tag == 'ee':
                print(i)
                print('url: ', c.text)
                
                try:
                    response = urlopen(c.text, timeout = 2)
                    html = response.read()
                    if html != '':
                        parser = MyHTMLParser()
                        parser.feed(str(html))
                    
                        new = Element('summary')
                        new.text = parser.get_data()
                        child.append(new)
                    else:
                        print('No content\n')
                except:
                    print('Error processing link, skipping\n')

print('Fetch complete')
print('Writing to new file')

#Writing to the final xml
tree.write('dblp.xml', encoding = 'utf-8', xml_declaration = True)

print('Complete')
