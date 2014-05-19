# created a list of suggested names given an arxiv number

from urllib import urlopen
import xml.etree.ElementTree as ET
import cPickle as pickle
import numpy as np

def subsplit(words, string):
    res = []
    for word in words:
        res.extend(word.split(string))
    return res

def eliminate_empty(words):
    return [word for word in words if len(word) > 0]

def str2list(string):
    words = string.split(' ')
    words = subsplit(words, '\n')
    words = eliminate_empty(words)
    return words

def list2wdict(words):
    wdict = {}
    for word in words:
        if word in wdict.keys():
            wdict[word] += 1
        else:
            wdict[word] = 1
    return wdict

def abs2vector(url):
    root = ET.parse(urlopen(url)).getroot()
    prefix= "{http://www.w3.org/2005/Atom}"

    res = ''
    for entry in root.findall(prefix+'entry'):
        res += entry.find(prefix+'title').text
        res += entry.find(prefix+'summary').text

    res = str2list(res)
    res = list2wdict(res)
    return res

def get_metric(wdict):
    res = {}
    for key, value in wdict.iteritems():
        res[key] = 1. / value**2
    return res
        
def prod(g, a, b):
    res = 0.
    for key, value in b.iteritems():
        val = g.get(key, 0.) * a.get(key, 0.) * value
        #if key in g and key in a:
        #    print '%s\t\t %.5f' % (key, val)
        res += val
    return res

def suggest_people(arxiv_id, people_fn='kipackizens.pkl', thres=0.1):
    pfile = open(people_fn)
    people_dict = pickle.load(pfile)
    all_word_dict = people_dict.pop('All words')
    g = get_metric(all_word_dict)
    
    url = 'http://export.arxiv.org/api/query?id_list='+arxiv_id+'&max_results=1'
    abs_dict = abs2vector(url)

    dt = np.dtype([('person', np.str_, 40),('rank', float)])
    ranks = np.zeros(len(people_dict), dtype=dt)

    npeople = 0
    for i, person in enumerate(people_dict.keys()):
        #print person
        rank = prod(g, people_dict[person]['keywords'], abs_dict)
        ranks[i] = (person, rank)
        if rank > thres:
            npeople += 1
        #print
    ranks = np.sort(ranks, order='rank')[::-1]
    
    return ranks[:npeople]

if __name__ == '__main__':
    import sys
    print suggest_people(sys.argv[1])
