

import xml.etree.ElementTree as ET
tree = ET.parse('data.xml')
root = tree.getroot()

prefix= "{http://www.w3.org/2005/Atom}"
for entry in root.findall(prefix+'entry'):
    a = entry.find(prefix+'title').text;
    print a.encode('utf-8');
    b = entry.find(prefix+'summary').text;
    b = b.replace('\n', ' ');
    print b
