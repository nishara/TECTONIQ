# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"


import pymongo
from gensim.utils import lemmatize
from nlplib.clean_text import CleanText
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
import time



client = pymongo.MongoClient()
db = client['Tectoniq']
cleanText = CleanText()

function = """function(){
				var items = db.search_index2.find().addOption(DBQuery.Option.noTimeout);
				while(items.hasNext()){
				var item = items.next();
					doc = {word: item._id, docIDs: item.value.docIDs};
					db.search_index.insert(doc);
				}
			}"""

mapFunction = """function() {
				var key = this.word;
				for (var idx=0; idx<this.docIDs.length; idx++){
					var tfidf = this.idf * this.docIDs[idx].tf;
					value = { 'docID': this.docIDs[idx].docID, 'TFIDF': tfidf };
					emit(key, {'docIDs': [value]});
				}
			}"""

reduceFunction = """function(key, values){
				var result = {'docIDs': []};
				values.forEach(function(v){
					result.docIDs = v.docIDs.concat(result.docIDs);
				});
				return result;
			}"""

class Search:
	def score(self, word):
		db.search_index2.drop()
		db.search_index.drop()
		db.vocabulary.map_reduce(mapFunction, reduceFunction, 'search_index2', query={'word': word})
		db.eval(function)
		response = db.search_index.find({'word': word}, {'docIDs': 1, '_id': 0})
		lista = {}
		for value in response[0]['docIDs']:
			lista[value['docID']] = value['TFIDF']
		db.search_index2.drop()
		db.search_index.drop()
		return lista

	def rank(self, searchPhrase):
		keys = []
		scorePhrase = {}
		for word in searchPhrase:
			if not keys:				
				keys = self.listSearch[word].keys()
			else:
				keys = list(set(keys) & set(self.listSearch[word].keys()))
		for key in keys:
			score = 0
			for word in searchPhrase:
				score += self.listSearch[word][key]
			scorePhrase[key] = round(score, 2)
		#print searchPhrase, scorePhrase
		return scorePhrase, keys


	def __init__(self, searchPhrase, k=0):
		self.words = [word.split('/')[0] for word in lemmatize(cleanText.removeStopWords(cleanText.cleanText(searchPhrase)[0]))]
		self.listSearch = {}
		self.k = k

	def results(self):
		no_threads = cpu_count()
		no_results = []
		with ThreadPoolExecutor(max_workers = no_threads) as e:
			for word in self.words:
				result = e.submit(self.score, word)
				try:
					self.listSearch[word] = result.result()
				except:
					no_results.append(word)
					print "no results",

		for word in no_results:
			self.words.remove(word)

		keys = {}
		rankedPhrase = {}
		w = ' '.join(word for word in self.words)
		rankedPhrase[w], keys[w] = self.rank(self.words)
				
		distinctKeys = []
		for key in keys:			
			distinctKeys += keys[key]
		distinctKeys =list(set(distinctKeys))


		answer = {}
		for key in distinctKeys:
			if rankedPhrase[w].get(key, -1) != -1:
				answer[key] = max(rankedPhrase[w][key], answer.get(key, -1))
		
		if self.k !=0:
			answer = dict(sorted(answer.items(), key=lambda x: x[1], reverse=True)[:self.k])
		else:
			answer = dict(sorted(answer.items(), key=lambda x: x[1], reverse=True))
		l = []
		for key in answer:
			d={}
			d = db.documents.find_one(spec_or_id={"_id": key})
			l.append({ 'recordId': d['record_id'], 'title': d['title'], 'description': d['description'], 'score':answer[key] })
		return l

"""
if __name__ == "__main__":
	db.search_index.drop()
	searchPhrase = []
	searchPhrase.append("fuck shit")


	time_words = []
	for j in range(0, 1):
		start = time.time()
		search = Search(searchPhrase[0], 20000)
		search.results()
		end = time.time() 
		time_words.append(end-start)
	print "no search words: k = ", 20, 'mean time:', round(sum(time_words)/len(time_words), 2)
"""
