__author__ = 'Nishara'

import random
import string

from nltk.corpus import wordnet as wn
import cherrypy
import rdflib


class Search(object):
    def __init__(self, rdf):
        if not rdf:
            print("Please specify an RDF file")
        self.g = rdflib.Graph()
        try:
            self.g.parse(rdf)
        except:
            print("{0:s} is not a valid rdf file.".format(rdf))
            quit()
        self.details = self.getBykeyword()
        print(self.details)

    @cherrypy.expose
    def index(self):
        return "Tectoniq Filtering"

    def getBykeyword(self):
        q = "PREFIX tectoniq:<http://www.semanticweb.org/nishara/ontologies/2015/4/tectoniq#> " \
            "SELECT ?name ?description WHERE {{?name tectoniq:hasDescription ?description }}"
        r = self.g.query(q)
        cat = []
        for i in r:
            cat.append(i[0])
        return cat

if __name__ == '__main__':
    rdf_file = "output.owl"
    cherrypy.quickstart(Search(rdf=rdf_file))