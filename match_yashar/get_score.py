
import numpy as np
import os
from os.path import basename
from collections import defaultdict

x = np.genfromtxt("abstract_vector.txt", dtype=None)
x = np.float32(x)
norm_x = np.divide(x,np.sum(x));

L = {}
d = {}
w = defaultdict(list);

# directory where member keyword data are stored
indir = 'data'
for root, dirs, filenames in os.walk(indir):
    for f in filenames:
	y = np.genfromtxt(os.path.join(root, f), dtype=None)
	y = np.float32(y)
	#norm_y = np.divide(y,np.sum(y));
        #for j in range(0, len(norm_y)):
        #         if norm_y[j]>0.1: norm_y[j]=0.1
        norm_y = y;
        #norm_y = np.divide(y,10);
        word_scores = norm_x*norm_y;
        author = os.path.splitext(f)[0];
        score = np.dot(norm_x, norm_y);
	#print author;
        #print score;
        d[author] = score;
        #print word_scores
        for word_sc in word_scores:
                w[author].append(word_sc)

presenters = sorted(d, key=lambda k: d[k], reverse=True); 


with open("standard_keywords.txt") as ff:
    keywords = ff.readlines()

#words = sorted(d, key=lambda k: w[f][k], reverse=True);

for f in presenters:
     wordscores = w[f];
     num_matched_words =  len(sum(np.nonzero(wordscores)))
     #words = sorted(words, key=lambda k: words[k], reverse=True);
     print f, d[f]
     #for j in range(0, len(wordscores)):
     #             L[keywords[j]]=wordscores[j];
     #topwords = sorted(L, key=lambda k: L[k], reverse=True);
     #print topwords[:num_matched_words]
     #print 
