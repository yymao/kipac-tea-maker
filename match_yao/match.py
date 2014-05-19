#!/usr/bin/env python
import cgi
import cPickle as pickle
from match_lib import *
form = cgi.FieldStorage()
arxiv_id = form.getvalue('id')

print "Content-Type: text/plain"
print 

try:
    if not arxiv_id:
        raise ValueError

    with open('people.pkl') as f:
        people = pickle.load(f)

    title, scores = match(arxiv_id, people, 0.6)
    indices = sorted(xrange(len(scores)), key=lambda i: scores[i], reverse=True)

    if form.getvalue('list'):
        print title
        print
        for i in indices:
            print people[i]['name'], scores[i]
    else:
        names = []
        for j, i in enumerate(indices):
            if j >= 4:
                break
            if scores[i] > 0.02:
                names.append(people[i]['name_short'])
        print ', '.join(names) if len(names) else 'Found no one!'

except Exception as e:
    print 'Error!', e

