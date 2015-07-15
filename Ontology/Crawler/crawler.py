__author__ = 'Nishara'

from xml.dom.minidom import Document
from xml.dom import minidom
from os.path import isfile, join
from os import listdir
import xml.etree.ElementTree as ET
import codecs



class InstanceGenerator():
    nodesToAttach = []
    doc = Document()
    prefix = "http://www.semanticweb.org/nishara/ontologies/2015/4/tectoniq#"

    # def __init__(self, ontology, populatedOutput):
    #     self.ontology = ontology
    #     self.populatedOutput = populatedOutput

    def generate(self):
        directory = 'J:/Semester 3/Internship Work/Data/IRHIS_BaseImages'
        filename = 'VdBmonMorts13-02_caption.xml'

        tree = ET.parse(join(directory, filename))
        root = tree.getroot()
        id = root.attrib.get("record_id")
        for child in root.findall("./description"):
            title = child.find("TitreEnregistrement").text
            description = child.find("Description").text
            l_keywords = set()

            for keyword in child.findall("MotsClefsAnalytiques"):
                l_key = [word.strip() for word in keyword.text.split(";")]
                l_keywords.update(set(l_key))
            l_locations = set()
            for keyword in child.findall("MotsClefsGeographiques"):
                l_loc = [word.strip() for word in keyword.text.split(";")]
                l_locations.update(set(l_loc))

            period = {"Epoch": child.find("EpoqueEvenement").text}
            if child.find("AnneeEvenement") is not None:
                period["Year"] = child.find("AnneeEvenement").text

            source = {}
            if child.find("ReferenceBibliographique") is not None:
                source["Book"] = child.find("ReferenceBibliographique").text
            if child.find("ProvenanceDocument") is not None:
                source["Depository"] = child.find("ProvenanceDocument").text
            if child.find("EtablissementDepositaire") is not None:
                source["Institution"] = child.find("EtablissementDepositaire").text

            photo = child.find("CodePhoto").text
            toAttach = self.createImage("image_" + id, title, description, l_keywords, l_locations, period, source,
                                        photo)
            self.attachToFile(toAttach)

    def createImage(self, id, title, description, keywords, locations, period, source, photo):
        linkedIndividuals = []
        ind = self.createNode("NamedIndividual")
        ind.setAttribute("rdf:about", self.prefix + id)

        instanceOf = self.createNode("rdf:type")
        instanceOf.setAttribute("rdf:resource", self.prefix + "Image")
        ind.appendChild(instanceOf)

        ind.appendChild(self.createDataPropertyNode(title, "hasTitle"))
        ind.appendChild(self.createDataPropertyNode(description, "hasDescription"))

        if keywords:
            for key in keywords:
                keyWithoutSpaces = key.replace(" ", "_").lower()
                linkedIndividuals.append(self.createLinkedType(keyWithoutSpaces, "Keyword", key, "hasKey"))
                keyPropNode = self.createNode("hasKeyword")
                keyPropNode.setAttribute("rdf:resource", self.prefix + keyWithoutSpaces)
                ind.appendChild(keyPropNode)

        if locations:
            for loc in locations:
                linkedIndividuals.append(self.createLinkedType(loc.lower(), "Location", loc, "hasLocation"))
                locationPropNode = self.createNode("describesLocation")
                locationPropNode.setAttribute("rdf:resource", self.prefix + loc)
                ind.appendChild(locationPropNode)

        if period:
            i = 1
            for key, value in period.items():
                indName = key.lower()+ str(i) + "10"
                resourceType = key
                property = "has" + key
                linkedIndividuals.append(self.createLinkedType(indName, resourceType, value, property))
                periodPropNode = self.createNode("belongsToPeriod")
                periodPropNode.setAttribute("rdf:resource", self.prefix + indName)
                ind.appendChild(periodPropNode)
                i += 1

        if source:
            i = 1
            for key1, value1 in source.items():
                indName = key1.lower() + str(i)+ "10"
                resourceType = key1
                property = "has" + key1
                linkedIndividuals.append(self.createLinkedType(indName, resourceType, value1, property))
                sourcePropNode = self.createNode("isFromSource")
                sourcePropNode.setAttribute("rdf:resource", self.prefix + indName)
                ind.appendChild(sourcePropNode)
                i += 1

        photoNode = self.createNode("hasPhoto")
        text = self.doc.createTextNode(photo)
        photoNode.appendChild(text)
        ind.appendChild(photoNode)

        linkedIndividuals.append(ind)

        return linkedIndividuals

    def createNode(self, nodeName):
        return self.doc.createElement(nodeName)

    def createLinkedType(self, individualName, resource, literalValue, propertyName):
        node = self.createNode("NamedIndividual")
        node.setAttribute("rdf:about", self.prefix + individualName)
        concept = self.createNode("rdf:type")
        concept.setAttribute("rdf:resource", self.prefix + resource)
        node.appendChild(concept)
        node.appendChild(self.createDataPropertyNode(literalValue, propertyName))
        return node

    def createDataPropertyNode(self, dataValue, property):
        dataValueNode = self.createNode(property)
        text = self.doc.createTextNode(dataValue)
        dataValueNode.appendChild(text)
        return dataValueNode

    def attachToFile(self, nodesToAttached):
        ontology = open('J:/Semester 3/Internship Work/TECTONIQ/Ontology/tectoniq.owl', 'r')
        xml_doc = minidom.parse(ontology)
        rdf = xml_doc.getElementsByTagName("rdf:RDF")[0]


        # print (rdf.toprettyxml(indent="  ", encoding="utf-8"))
        for node in nodesToAttached:
            rdf.appendChild(node)
        ontology.close()

        f = codecs.open('output.owl', mode='w', encoding='utf-8')
        xml_doc.writexml(f, indent="  ", addindent="  ", newl='\n')
        f.close()


if __name__ == '__main__':
    # fuseki-server --update --mem /ds
    ig = InstanceGenerator()
    ig.generate()
