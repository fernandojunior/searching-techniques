'''
Parse an instance of TSPLIB from XML format to JSON format.

http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html
http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/XML-TSPLIB/instances/
https://docs.python.org/2/library/xml.etree.elementtree.html
http://stackoverflow.com/questions/12309269/write-json-data-to-file-in-python

@author Fernando Felix do Nascimento Junior
'''

import collections
from xml.etree import ElementTree
import json

instance_container = 'data'
instance_name = 'brazil58'
instance_path = '%s/%s' % (instance_container, instance_name)
input_instance = '%s.xml' % instance_path
output_instance = '%s.json' % instance_path

tree = ElementTree.parse(input_instance)
root = tree.getroot()

vertices = {}

count = 0

for vertex in root.iter('vertex'):
    edges = {}
    for edge in vertex.iter('edge'):
        position = int(edge.text)
        cost = float(edge.attrib['cost'])
        edges[position] = cost
    vertices[count] = edges
    count = count + 1

# ordering
vertices = collections.OrderedDict(sorted(vertices.items()))

print(list(vertices.keys()))
# print(vertices)

with open(output_instance, 'w') as f:
    json.dump(vertices, f, indent=4, sort_keys=True)
