'''
Parse instances of TSPLIB from XML format to python dict format or JSON format.

http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/index.html
http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/XML-TSPLIB/instances/
https://docs.python.org/2/library/xml.etree.elementtree.html
http://stackoverflow.com/questions/12309269/write-json-data-to-file-in-python

@author Fernando Felix do Nascimento Junior
'''

from xml.etree import ElementTree
import csv
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
        vertices_from_xml = self.instance[5].findall('vertex')
        size = len(vertices_from_xml)

        distances = {}

        # looking up xml vertices
        for i in range(size):
            vertex = vertices_from_xml[i]
            edges = {}
            edges[i] = 0  # if i = j then cost = 0

            # looking up current vertex edges
            for edge in vertex.iter('edge'):
                j = int(edge.text)  # vertex target position
                cost = float(edge.attrib['cost'])  # edge cost/distance
                edges[j] = cost

            distances[i] = edges

        return distances

    def to_matrix(self):
        vertices_from_xml = self.instance[5].findall('vertex')
        size = len(vertices_from_xml)

        # matrix initialized to 0
        distances = [[0 for x in range(size)] for x in range(size)]

        # looking up xml vertices
        for i in range(size):
            vertex = vertices_from_xml[i]

            # looking up current vertex edges
            for edge in vertex.iter('edge'):
                j = int(edge.text)  # vertex target position
                cost = float(edge.attrib['cost'])  # edge cost/distance
                distances[i][j] = cost  # edges distances

        return distances

    def to_csv(self, filename=''):

        if filename == '':
            filename = '%s.csv' % self.instance_name

        with open(filename, 'a') as f:
            writer = csv.writer(
                f, delimiter=',',
                quoting=csv.QUOTE_MINIMAL,
                lineterminator='\n')

            distances = self.to_matrix()

            # header: writer.writerow([i for i in range(len(distances))])
            for item in distances:
                writer.writerow(item)

    def to_json(self, indent=4, sort_keys=True):
        return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys)

    def json_dump(self, filename='', indent=4, sort_keys=True):

        if filename == '':
            filename = '%s.json' % self.instance_name

        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=indent, sort_keys=sort_keys)
