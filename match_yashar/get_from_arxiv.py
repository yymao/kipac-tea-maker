import urllib
url = 'http://export.arxiv.org/api/query?search_query=au:+AUTHOR&start=0&max_results=100'
data = urllib.urlopen(url).read()
print data

