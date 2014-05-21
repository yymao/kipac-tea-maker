urls = """
http://kipac.stanford.edu/kipac/views/ajax?field_person_display_name_value=&type=2841&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_args=&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0
http://kipac.stanford.edu/kipac/views/ajax?js=1&page=1&type=2841&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0&view_args=
http://kipac.stanford.edu/kipac/views/ajax?field_person_display_name_value=&type=2836&field_person_membership2_nid=2813&location=All&view_name=people_list&view_display_id=page_1&view_args=&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0
http://kipac.stanford.edu/kipac/views/ajax?js=1&page=1&type=2836&field_person_membership2_nid=2813&location=All&view_name=people_list&view_display_id=page_1&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0&view_args=
http://kipac.stanford.edu/kipac/views/ajax?field_person_display_name_value=&type=2834&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_args=&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0
http://kipac.stanford.edu/kipac/views/ajax?js=1&page=1&type=2834&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0&view_args=
http://kipac.stanford.edu/kipac/views/ajax?field_person_display_name_value=&type=3032&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_args=&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0
http://kipac.stanford.edu/kipac/views/ajax?field_person_display_name_value=&type=2837&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_args=&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0
http://kipac.stanford.edu/kipac/views/ajax?js=1&page=1&type=2837&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0&view_args=
http://kipac.stanford.edu/kipac/views/ajax?js=1&page=2&type=2837&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0&view_args=
http://kipac.stanford.edu/kipac/views/ajax?field_person_display_name_value=&type=2833&field_person_membership2_nid=All&location=All&view_name=people_list&view_display_id=page_1&view_args=&view_path=people&view_base_path=people&view_dom_id=2&pager_element=0
""".splitlines()[1:]

import re
from urllib import urlopen
import cPickle as pickle

re_name = re.compile(r'/kipac/people/\w+\\\"\\x3e([\w\s-]+)\\x3c')

def change_name_fmt(name):
    if name == 'Matthew Becker':
        return 'Matt B', 'Becker_Matthew'
    elif name == 'Chris Davis':
        return 'Chris D', 'Davis_C_P'
    elif name == 'Yashar Hezavehe':
        return 'Yashar H', 'Hezaveh_Y'
    elif name == 'Bryant Garcia':
        return 'Bryant G', 'Garcia_Bryant'
    elif name == 'Chao-Lin Kuo':
        return 'Chao-Lin', 'Kuo_C_L'
    elif name == 'Kimmy Wu':
        return 'Kimmy W', 'Wu_W_L_K'
    item = name.split()
    first = item[:-1]
    last = item[-1]
    if first[-1] == 'da':
        first = first[:-1]
        last = 'da ' + last
    last = re.sub('\W', '_', last)
    first = ' '.join(first)
    fmt1 = first + ' ' + last[0]
    first = re.split('\W', first)
    if len(last) <= 4:
        first = '_'.join(first)
    else:
        first = '_'.join(map(lambda s:s[0], first))
    fmt2 = last + '_' + first
    return fmt1, fmt2

people = []
for url in urls:
    for m in re_name.finditer(urlopen(url).read()):
        name = m.groups()[0]
        name_short, name_arxiv = change_name_fmt(name)
        people.append({'name':name, 'name_short':name_short, \
                'name_arxiv':name_arxiv})

with open('people.pkl', 'w') as fo:
    pickle.dump(people, fo)

