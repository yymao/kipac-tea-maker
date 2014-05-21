from match_lib import *
import cPickle as pickle

url_base = 'http://export.arxiv.org/api/query?search_query=cat:astro-ph*+AND+au:%s&max_results=50&sortBy=submittedDate&sortOrder=descending'

with open('../kipac-people/people.pkl', 'r') as f:
    people = pickle.load(f)

new_people = []
for person in people:
    root = get_arxiv_xml_root(url_base%person['name_arxiv'])
    wfd_all = {}
    bfd_all = {}
    count = 0
    for entry in root.findall(xml_prefix+'entry'):
        title = entry.find(xml_prefix+'title').text
        if title == 'Error':
            continue
        count += 1
        wfd, bfd = get_grams(title, entry.find(xml_prefix+'summary').text)
        wd_count = float(sum(wfd.itervalues()))
        bg_count = wd_count - 2.0
        for k in wfd:
            wfd_all[k] = wfd_all.get(k, 0) + wfd[k]/wd_count
        for k in bfd:
            bfd_all[k] = bfd_all.get(k, 0) + bfd[k]/bg_count
    count_f = float(count)
    for k in wfd_all:
        wfd_all[k] /= count_f
    for k in bfd_all:
        bfd_all[k] /= count_f
    person['count'] = count
    person['wfd'] = wfd_all
    person['bfd'] = bfd_all
    if count:
        new_people.append(person)
    print person['name'], person['name_arxiv'], person['count']

with open('people.pkl', 'w') as fo:
    pickle.dump(new_people, fo)

