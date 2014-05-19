# create a dictionary of people in KIPAC
import tea_arxiv as ta
import cPickle as pickle

with open('../kipac-people/people.pkl', 'r') as f:
    people = pickle.load(f)

tot_dict = {'All words':{}}
url_base = 'http://export.arxiv.org/api/query?search_query=cat:astro-ph*+AND+au:%s&max_results=10&sortBy=submittedDate&sortOrder=descending'
for person in people:
    tot_dict[person['name']] = {'keywords': \
            ta.abs2vector(url_base%person['name_arxiv'])}
    for word in tot_dict[person['name']]['keywords']:
        tot_dict['All words'][word] = tot_dict['All words'].get(word, 0) \
                + tot_dict[person['name']]['keywords'][word]

with open('kipackizens.pkl', 'w') as f:
    pickle.dump(tot_dict, f)

