__author__ = 'Nishara'

from os import listdir
from os.path import isfile, join
from pymongo import MongoClient
import xml.etree.ElementTree as ET

import re
import sys


class Parser(object):

    def images(self):
        directory = 'J:/Semester 3/Internship Work/Data/IRHIS_BaseImages'
        xml_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.xml')]

        cl = MongoClient()
        coll = cl["Tectoniq"]["images"]

        for filename in xml_files:
            tree = ET.parse(join(directory, filename))
            root = tree.getroot()
            doc = {}
            doc["record_id"] = root.attrib.get("record_id")

            for event in root.findall("./description"):

                for c in event.getchildren():
                    if c.tag in doc.keys():
                        if not isinstance(doc[c.tag], list):
                                doc[c.tag] = [doc[c.tag]]
                                doc[c.tag].append(c.text)
                        else:
                            doc[c.tag].append(c.text)
                        print doc[c.tag]
                    else:
                        doc[c.tag] = c.text


                coll.update({"record_id":root.attrib.get("record_id")},doc, upsert=True)

    def inventories(self):
        directory = 'J:\Semester 3\Internship Work\Data\ServiceInventaire\ServiceInventaire'
        xml_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.xml')]

        cl = MongoClient()
        coll = cl["Tectoniq"]["inventories"]

        for filename in xml_files:
            tree = ET.parse(join(directory, filename))
            root = tree.getroot()
            document = {}
            document["reference_id"] = root.attrib.get("reference")

            for event in root.findall("."):

                for c in event.getchildren():
                    if c.tag in document.keys():
                        if not isinstance(document[c.tag], list):
                                document[c.tag] = [document[c.tag]]
                                document[c.tag].append(c.text)
                        else:
                            document[c.tag].append(c.text)
                        print document[c.tag]
                    else:
                        document[c.tag] = c.text


                coll.update({"reference_id":root.attrib.get("reference")},document, upsert=True)

    def vdn(self):
        directory =  'J:/Semester 3/Internship Work/Data/LaVoixDuNord/LaVoixDuNord/'
        xml_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.xml')]

        cl = MongoClient()
        coll = cl["Tectoniq"]["vdn"]

        for filename in xml_files:
            tree = ET.parse(join(directory, filename))
            root = tree.getroot()
            document = {}

            for event in root.findall("./DOCUMENT"):
                document["document_id"] = event.attrib.get("id")
                for c in event.getchildren():
                    if len(c._children) > 1:
                        for subc in c._children:
                            if subc.tag in document.keys():
                                if not isinstance(document[subc.tag], list):
                                    document[subc.tag] = [document[subc.tag]]
                                    document[subc.tag].append(subc.text)
                                else:
                                    document[subc.tag].append(subc.text)
                            else:
                                document[subc.tag] = subc.text

                    else:
                        if c.tag in document.keys():
                            if not isinstance(document[c.tag], list):
                                    document[c.tag] = [document[c.tag]]
                                    document[c.tag].append(c.text)
                            else:
                                document[c.tag].append(c.text)
                        else:
                            document[c.tag] = c.text

                coll.update({"document_id":event.attrib.get("id")},document, upsert=True)

    def get_db(self):
        client = MongoClient('localhost:27017')
        db = client.Tectoniq
        return db

if __name__ == '__main__':
    parser = Parser()

    # Connection to Mongo DB
    try:
        db = parser.get_db()
        collections = db.collection_names()

        for coll in collections:
            if coll.encode('utf-8') == 'images':
                # context = db.images.find({}, {"MotsClefsAnalytiques": 1, "record_id": 1, "CodePhoto": 1})
                # for res in context:
                    # for item in res["MotsClefsAnalytiques"]:
                    #     if re.search("entreprise", item):
                    #         print res["record_id"], res["CodePhoto"]

                result = db.images.find({}, {"$text": {"$search": "entreprise"}})
                for res in result:
                    print res["record_id"]
        # for res in result:
        #     print res['EpoqueEvenement']
        #
        # for line in open(file, 'r'):
    		# if re.search(sys.argv[1], line):
    		# 	print line


    except Exception, e:
        print "Could not connect to MongoDB: %s" % e
    # parser.images()
    # parser.inventories()
    # parser.vdn()
