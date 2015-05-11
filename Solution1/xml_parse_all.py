# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

from os import listdir
from os.path import isfile, join
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from nlplib.clean_text import CleanText
from nlplib.lemmatize_text import LemmatizeText
from indexing.vocabulary_index import VocabularyIndex as VI

import re
import sys



class Parser(object):
    def __init__(self, dbname):
        self.dbname = dbname
        self.documents = []
        self.client = MongoClient()
        self.db = self.client[self.dbname]
        self.ct = CleanText()


    def images(self):
        directory = '../../DATA_SETS/IRHIS_BaseImages/'
        xml_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.xml')]
        
        for filename in xml_files:
            tree = ET.parse(join(directory, filename))
            root = tree.getroot()
            document = {}
            if root.attrib.get("record_id"):
                document["record_id"] = root.attrib.get("record_id").strip()
                for child in root.findall("description"):
                    document["title"] = self.ct.cleanText(child.find("TitreEnregistrement").text, "FR")[0]
                    document["description"] = self.ct.cleanText(child.find("Description").text, "FR")[0]
                    document["epoch"] = [child.find("EpoqueEvenement").text]
                    document["photo"] = child.find("CodePhoto").text
                    if child.find("ReferenceBibliographique") is not None:
                        document["reference"] = child.find("ReferenceBibliographique").text
                    if child.find("ProvenanceDocument") is not None:
                        document["source"] = child.find("ProvenanceDocument").text
                    if child.find("EtablissementDepositaire") is not None:
                        document["source_location"] = child.find("EtablissementDepositaire").text
                    if child.find("AnneeEvenement") is not None:
                        document["date"] = child.find("AnneeEvenement").text
                    words = self.getWords(document["description"])
                    if words:
                        document['words'] = words
                    l = set()
                    for a in child.findall("MotsClefsAnalytiques"):
                        l.add(a.text)
                    document["keywords"] = list(l)
                    l = set()
                    for a in child.findall("MotsClefsGeographiques"):
                        l.add(a.text)
                    document["location"] = list(l)
                self.documents.append(document)

    def insert(self):
        self.db.document.drop()
        if self.documents:
            self.db.documents.insert(self.documents)
        vocab = VI(self.dbname)
        vocab.createIndex()

           
    def getWords(self, text):
        lemmas = LemmatizeText(self.ct.removePunctuation(text), "FR")
        lemmas.createLemmaText()
        lemmaText = lemmas.cleanText
        words = []
        if lemmaText and lemmaText != " ":
            lemmas.createLemmas()
            for w in lemmas.wordList:
                word = {}
                word['word']=w.word
                word['tf']=w.tf
                word['count']=w.count
                word['pos']=w.wtype
                words.append(word)
        return words

    def inventories(self):
        directory = '../../DATA_SETS/ServiceInventaire/'
        xml_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.xml')]
        for filename in xml_files:
            tree = ET.parse(join(directory, filename))
            root = tree.getroot()
            document = {} 
            if root.attrib.get("reference"):
                document["record_id"] = root.attrib.get("reference").strip()
                document["title"] = self.ct.cleanText(root.find("edifice").text, "FR")[0]
                document["description"] = self.ct.cleanText(root.find("historique").text, "FR")[0] + ' ' + ' '.join(self.ct.cleanText(root.find("historique").text, "FR")[0].split(';'))
                document["keywords"] = []
                if root.find("denomination").text is not None:
                    document["keywords"] += root.find("denomination").text.split(";")
                if root.find("grosOeuvres").text is not None:
                    document["keywords"] += root.find("grosOeuvres").text.split(";")
                if root.find("materiauxCouverture").text is not None:
                    document["keywords"] += root.find("materiauxCouverture").text.split(";")
                if root.find("couvrement").text is not None:
                    document["keywords"] += root.find("couvrement").text.split(";")
                document["epoch"] = root.find("epoqueConstruction").text.split(";")
                document["location"] = root.find("localisation").text.split(";")
                words = self.getWords(document["description"])
                if words:
                    document['words'] = words
                self.documents.append(document)
        
    def vdn(self):
        directory =  '../../DATA_SETS/LaVoixDuNord/'
        xml_files = [f for f in listdir(directory) if isfile(join(directory, f)) and f.endswith('.xml')]

        for filename in xml_files:
            tree = ET.parse(join(directory, filename))
            root = tree.getroot()

            for child in root.findall('DOCUMENT'):
                key = 'document_' + child.attrib.get("id")
                document = {}
                document['record_id'] = key
                document['source'] = child.find('DESCRIPTION').find('SOURCE').text
                document['author'] = child.find('DESCRIPTION').find('AUTEUR').text
                document['source_location'] = child.find('DESCRIPTION').find('REFERENCE').text
                document['date'] = child.find('DESCRIPTION').find('DATE').text
                document['title'] = self.ct.cleanText(child.find('DESCRIPTION').find('TITRE').text, "FR")[0]
                document['description'] = self.ct.cleanText(child.find('TEXTE').text, "FR")[0]
                words = self.getWords(document["description"])
                if words:
                    document['words'] = words
                self.documents.append(document)
        
if __name__ == '__main__':
    parser = Parser("Tectoniq")
    parser.images()
    parser.inventories()
    parser.vdn()
    parser.insert()

