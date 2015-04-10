# coding: utf-8
import yaml
from os import listdir
from os.path import isfile, join
import sys
from collections import Counter, OrderedDict

reload(sys)
sys.setdefaultencoding('utf8')

mypath = 'J:/Semester 3/Internship Work/Data/IRHIS_BaseImages'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith('.yml')]

d = {}
l = {}
# print len(onlyfiles)
idx = 1

# get the files that have information about the similart item
for filename in onlyfiles:
    record = 'record' + str(idx)
    stream = open(join(mypath, filename), "r")
    docs = yaml.load_all(stream)
    for doc in docs:
        for v1 in doc.values():
            for v2 in v1.values():
                if d:
                    ok = True
                    for key, value in d.iteritems():
                        if value['Description'].strip() == v2['Description'].strip():
                            if v2.get('ReferenceBibliographique') and value.get('ReferenceBibliographique'):
                                if value['ReferenceBibliographique'].strip() == v2['ReferenceBibliographique'].strip():
                                    ok = False
                            if v2.get('ProvenanceDocument') and value.get('ProvenanceDocument'):
                                if value['ProvenanceDocument'].strip() == v2['ProvenanceDocument'].strip():
                                    ok = False
                            if not ok:
                                l[key].append(filename)
                                break
                    if ok:
                        d[record] = v2
                        l[record] = [filename]
                        idx += 1
                else:
                    d[record] = v2
                    l[record] = [filename]
                    idx += 1
                #print '*****************'

#print len(d.keys())

"""
#test the list of similar files
for key, value in l.iteritems():
	print key, value
"""

final_dic = {}
idx = 1
for key, value in l.iteritems():
    if idx < 10:
        record = 'record0' + str(idx)
    else:
        record = 'record' + str(idx)

    for filename in value:
        stream = open(join(mypath, filename), "r")
        docs = yaml.load_all(stream)
        for doc in docs:
            for v1 in doc.values():
                for v2 in v1.values():
                    if final_dic.get(record, 0) == 0:
                        final_dic[record] = v2
                        final_dic[record]['CodePhoto'] = [final_dic[record]['CodePhoto']]
                    else:
                        final_dic[record]['CodePhoto'].append(v2['CodePhoto'])
                        print final_dic[record]['MotsClefsAnalytiques'], v2['MotsClefsAnalytiques']
                        print final_dic[record]['MotsClefsGeographiques'], v2['MotsClefsGeographiques']
                        l1 = list(set(final_dic[record]['MotsClefsAnalytiques'] + v2['MotsClefsAnalytiques']))
                        l2 = list(set(final_dic[record]['MotsClefsGeographiques'] + v2['MotsClefsGeographiques']))
                        final_dic[record]['MotsClefsAnalytiques'] = l1
                        final_dic[record]['MotsClefsGeographiques'] = l2


    idx += 1

final_dic = OrderedDict(sorted(final_dic.items()))

for key, value in final_dic.iteritems():
    print key
    for k2, v2 in value.iteritems():
        print k2, '->', v2
    print '*****************'

"""
aggdic = {}
for key1, value1 in d.iteritems():
	for key2, value2 in d.iteritems();
		if key1 != key2:
"""