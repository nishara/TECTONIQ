__author__ = 'Nishara'


from os.path import join
from os import *
from xml.etree import ElementTree
from xml2dict import XmlDictConfig

mypath = '.'


files = [f for f in listdir(mypath) if path.isfile(join(mypath, f)) and f.endswith('.xml')]

if __name__ == '__main__':

    elements = {}
    grouped_files = {}
    idx = 1

    for file in files:
        tree = ElementTree.parse(join(mypath, file))
        root = tree.getroot()
        xmldict = XmlDictConfig(root)
        record = 'record' + str(idx)

        if elements:
            ok = True
            for key, value in elements.iteritems():
                if value['epoqueConstruction'] == xmldict['epoqueConstruction']:
                    if xmldict.get('denomination') and value.get('denomination'):
                        if value['denomination'].strip() == xmldict['denomination'].strip():
                            ok = False
                        if xmldict.get('localisation') and value.get('localisation'):
                            if value['localisation'].strip() == xmldict['localisation'].strip():
                                ok = False
                        if not ok:
                            grouped_files[key].append(file)
                            break
                # if xmldict.get('typeEtude') and value.get('typeEtude'):
                #     if value['typeEtude'] == xmldict['typeEtude']:
                #         if xmldict.get('denomination') and value.get('denomination'):
                #             if value['denomination'].strip() == xmldict['denomination'].strip():
                #                 ok = False
                #             if xmldict.get('localisation') and value.get('localisation'):
                #                 if value['localisation'].strip() == xmldict['localisation'].strip():
                #                     ok = False
                #             if not ok:
                #                 grouped_files[key].append(file)
                #                 break
            if ok:
                elements[record] = xmldict
                grouped_files[record] = [file]
                idx += 1
        else:
            elements[record] = xmldict
            grouped_files[record] = [file]
            idx += 1

    print grouped_files

    # grosOeuvres
    # epoqueConstruction
    # typeEtude
    # denomination  : Important Tag
    # localisation
    # propriete
    # typeCouverture
