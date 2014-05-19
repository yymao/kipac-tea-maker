import re
from urllib import urlopen
import xml.etree.ElementTree as ET

stopwords = "a,about,above,after,again,against,all,am,an,and,any,are,aren't,as,at,be,because,been,before,being,below,between,both,but,by,can't,cannot,could,couldn't,did,didn't,do,does,doesn't,doing,don't,down,during,each,few,for,from,further,had,hadn't,has,hasn't,have,haven't,having,he,he'd,he'll,he's,her,here,here's,hers,herself,him,himself,his,how,how's,i,i'd,i'll,i'm,i've,if,in,into,is,isn't,it,it's,its,itself,let's,me,more,most,mustn't,my,myself,no,nor,not,of,off,on,once,only,or,other,ought,our,ours,ourselves,out,over,own,same,shan't,she,she'd,she'll,she's,should,shouldn't,so,some,such,than,that,that's,the,their,theirs,them,themselves,then,there,there's,these,they,they'd,they'll,they're,they've,this,those,through,to,too,under,until,up,very,was,wasn't,we,we'd,we'll,we're,we've,were,weren't,what,what's,when,when's,where,where's,which,while,who,who's,whom,why,why's,with,won't,would,wouldn't,you,you'd,you'll,you're,you've,your,yours,yourself,yourselves"
stopwords = stopwords.split(',')
stopwords.extend(['pc', 'kpc', 'mpc', 'gpc', 'et', 'al', 'au'])

url_base = 'http://export.arxiv.org/api/query?id_list=%s&max_results=1'
xml_prefix = '{http://www.w3.org/2005/Atom}'

def add_grams(text, wfd, bfd):
    last_w = None
    for m in re.finditer(r"[a-z][a-z-']*[a-z]", text, re.I):
        w = m.group().lower()
        if w not in stopwords:
            wfd[w] = wfd.get(w, 0) + 1
            if last_w is not None:
                bfd[last_w + ' ' + w] = bfd.get((last_w, w), 0) + 1
            last_w = w

def get_grams(*texts):
    wfd = {}
    bfd = {}
    for text in texts:
        add_grams(text, wfd, bfd)
    return wfd, bfd

def gram_prod(fd1, fd2):
    s = 0
    for k in fd1:
        s += fd1[k]*fd2.get(k, 0)
    return s

def get_arxiv_xml_root(query_url):
    return ET.parse(urlopen(query_url)).getroot()

def match(arxiv_id, people, weight=0.5):
    root = get_arxiv_xml_root(url_base%arxiv_id)
    entry = root.find(xml_prefix+'entry')
    title = entry.find(xml_prefix+'title').text
    if title == 'Error':
        raise ValueError

    wfd, bfd = get_grams(title, entry.find(xml_prefix+'summary').text)
    wd_count = float(sum(wfd.itervalues()))
    wfd_norm = reduce(lambda x,y:x+y*y, wfd.itervalues(), 0)/wd_count/(1.0-weight)
    bfd_norm = reduce(lambda x,y:x+y*y, bfd.itervalues(), 0)/(wd_count-2.0)/weight

    scores = [(gram_prod(wfd, person['wfd'])/wfd_norm
            + gram_prod(bfd, person['bfd'])/bfd_norm)*0.5 \
            for person in people]

    return title, scores

