# coding: utf-8
import string
import sys 
import re 
import codecs
import xml.etree.ElementTree as ET
"""
This is the parser for the news articles from the LaVoixDuNord corpus.
Keeps the text in utf8 encoding.
Removes replaces some specia characters.
"""
reload(sys)  
sys.setdefaultencoding('utf8')

specialchar_dic={
	"’": "'",
	"„": "\"",
	"“": "\"",
	"”": "\"",
	"«": "<<",
	"»": ">>",
	"…": "...",
	"–": "-",
	"¡": "!",
	"¿": "?"
}

specialchar_re = re.compile('(%s)' % '|'.join(specialchar_dic.keys()))

def replaceUTF8Char(text, specialchars = specialchar_dic):
	def replace(match):			
		return specialchars[match.group(0)]
	return specialchar_re.sub(replace, text)

tree = ET.parse('laVoixDuNord.xml')
root = tree.getroot()
d = {}

for child in root.findall('DOCUMENT'):
	key = 'document_' + child.attrib['id']
	d_int = {}
	d_int['source'] = replaceUTF8Char(child.find('DESCRIPTION').find('SOURCE').text.encode('utf8').lower()).replace('\n', ' ').strip()
	author = child.find('DESCRIPTION').find('AUTEUR').text.encode('utf8')
	d_int['author'] = replaceUTF8Char(string.capwords(author)).strip()
	d_int['url'] = replaceUTF8Char(child.find('DESCRIPTION').find('REFERENCE').text.encode('utf8').lower()).replace('\n', ' ').strip()
	d_int['date'] = replaceUTF8Char(child.find('DESCRIPTION').find('DATE').text.encode('utf8')).replace('\n', ' ').strip()
	d_int['title'] = replaceUTF8Char(child.find('DESCRIPTION').find('TITRE').text.encode('utf8')).replace('\n', ' ').strip()
	d_int['language'] = replaceUTF8Char(child.find('DESCRIPTION').find("PRESENTATION").find('LANGUE').text.encode('utf8')).replace('\n', ' ').strip()
	d_int['text'] = replaceUTF8Char(child.find('TEXTE').text.encode('utf8').strip()).replace('\n', ' ').strip()
	d[key] = d_int
	
for key, value in d.iteritems():
	print key
	for k2, v2 in value.iteritems():
		print k2, '->', v2
	print '*****************'