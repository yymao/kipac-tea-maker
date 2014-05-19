#!/usr/bin/env python
import cgi
form = cgi.FieldStorage()
arxiv_id = form.getvalue('id')

from tea_arxiv import *
print "Content-Type: text/plain"
print 

try:
    if not arxiv_id:
        raise ValueError

    ranks = suggest_people(arxiv_id, thres=0)

    if form.getvalue('list'):
        for r in ranks:
            print r['person'], r['rank']
    else:
        names = []
        for j, r in enumerate(ranks):
            if j >= 4:
                break
            if r['rank'] > 0.1:
                names.append(r['person'])
        print ', '.join(names) if len(names) else 'Found no one!'

except Exception as e:
    print 'Error!', e

