'''
Parse instances of TSPLIB from XML format to python dict format or JSON format.

http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html
http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/XML-TSPLIB/instances/
https://docs.python.org/2/library/xml.etree.elementtree.html
http://stackoverflow.com/questions/12309269/write-json-data-to-file-in-python

@author Fernando Felix do Nascimento Junior
'''

import collections
from xml.etree import ElementTree
import json


INSTANCE_CONTAINER = 'data'


class Parser:

    def __init__(self, instance_name):
        self.instance_name = '%s/%s' % (INSTANCE_CONTAINER, instance_name)
        input_instance = '%s.xml' % self.instance_name

        # XML parser
        tree = ElementTree.parse(input_instance)
        self.instance = tree.getroot()

    def to_dict(self):

        vertices = {}

        curr = 0  # vertex initial
        for vertex in self.instance.iter('vertex'):
            edges = {}

            for edge in vertex.iter('edge'):
                position = int(edge.text)  # vertex target position
                cost = float(edge.attrib['cost'])  # edge cost
                edges[position] = cost  # recording...

            # ordering vertex edges
            edges = collections.OrderedDict(sorted(edges.items()))

            # recording current vertex edges ...
            vertices[curr] = edges

            curr = curr + 1  # next vertex to be parsed

        # ordering vertices
        vertices = collections.OrderedDict(sorted(vertices.items()))

        return vertices

    def to_json(self, indent=4, sort_keys=True):
        return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys)

    def json_dump(self, filename='', indent=4, sort_keys=True):

        if filename == '':
            filename = '%s.json' % self.instance_name

        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=indent, sort_keys=sort_keys)


Parser('brazil58').json_dump()
Parser('eil101').json_dump()
Parser('gil262').json_dump()
