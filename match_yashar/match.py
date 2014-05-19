#!/usr/bin/env python
import cgi
form = cgi.FieldStorage()
arxiv_id = form.getvalue('id')

print "Content-Type: text/plain"
print 

try:
    import subprocess
    out = subprocess.check_output(['sh', 'score.sh', arxiv_id])

    if form.getvalue('list'):
        print out
    else:
        out = out.splitlines()
        names = []
        for j, i in enumerate(out):
            if j >= 4:
                break
            names.append(i.split()[0])
        print ', '.join(names) if len(names) else 'Found no one!'

except Exception as e:
    print 'Error!', e
