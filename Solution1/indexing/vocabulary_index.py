# coding: utf-8

__author__ = "Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "ciprian.truica@cs.pub.ro"
__status__ = "Production"

import pymongo


mapFunction = """function() {
					for (var idx=0; idx<this.words.length; idx++){
						var key = this.words[idx].word;
						var ids = {'docID': this._id, 'count': this.words[idx].count, 'tf': this.words[idx].tf, 'pos': this.words[idx].pos };
						var value = { 'ids': [ids]};
						emit(key, value);
					}
				}"""

reduceFunction = """function(key, values) {
						var result = {'ids': []};
						values.forEach(function (v) {
							result.ids = v.ids.concat(result.ids);
						});
						return result;
					}"""

functionCreate = """function(){
						var noDocs = db.documents.count();
						var start = new Date();
						var items = db.temp_collection.find().addOption(DBQuery.Option.noTimeout);
						while(items.hasNext()){
							var item = items.next();
							var n = item.value.ids.length;
							var widf = 1 + Math.round(Math.log(noDocs/n) * 100)/100;
							doc = {word: item._id, idf: widf, createdAt: new Date(), docIDs: item.value.ids};
							db.vocabulary.insert(doc);
						}
						db.temp_collection.drop();
					}"""
functionCreateQuery = """function(query){
						var noDocs = db.documents.count(query);
						var start = new Date();
						var items = db.temp_collection.find().addOption(DBQuery.Option.noTimeout);
						while(items.hasNext()){
							var item = items.next();
							var n = item.value.ids.length;
							var widf = 1 + Math.round(Math.log(noDocs/n) * 100)/100;
							doc = {word: item._id, idf: widf, createdAt: new Date(), docIDs: item.value.ids};
							db.vocabulary_query.insert(doc);
						}
						db.temp_collection.drop();
					}"""

functionUpdate ="""
					function(){
						var noDocs = db.documents.count();
						var words = db.vocabulary.find({},{_id: 0, word: 1, docIDs: 1}).addOption(DBQuery.Option.noTimeout);
						while(words.hasNext()){
							var word = words.next();
							var exists = db.temp_collection.findOne({word: word.word}, {docIDs: 1, _id:0});
							if (exists){
								var docIDs = exists.docIDs;
								docIDs = docIDs.concat(word.docIDs.length);
								var idf = Math.round(Math.log(noDocs/docIDs.length) * 100)/100;
								db.vocabulary.update({word: word.word}, {$set: {'idf': idf, docIDs: docIDs}});
								db.temp_collection.remove({_id: word.word});
							}else{
								var idf = Math.round(Math.log(noDocs/word.docIDs.length) * 100)/100;
								db.vocabulary.update({word: word.word}, {$set: {'idf': idf}});
							}
						}

						var items = db.temp_collection.find().addOption(DBQuery.Option.noTimeout);
						while(items.hasNext()){
							item = items.next();
							var widf = Math.round(Math.log(noDocs/item.value.ids.length) * 100)/100;
							doc = {word: item._id, idf: widf, createdAt: new Date(), docIDs: item.value.ids};
							db.vocabulary.insert(doc);
						}
						db.temp_collection.drop();
					}
				"""


functionDelete = """function (){
						var noDocs = db.documents.count();
						//update idf
						var words = db.vocabulary.find({},{_id: 0, word: 1, docIDs: 1}).addOption(DBQuery.Option.noTimeout);
						while(words.hasNext()){
							var word = words.next();
							var widf = Math.round(Math.log(noDocs/word.docIDs.length) * 100)/100;
							db.vocabulary.update({word: word.word}, {$set: {idf: widf}});
						}
					}"""


class VocabularyIndex:
	def __init__(self, dbname):
		client = pymongo.MongoClient()
		self.db = client[dbname]
	
	def createIndex(self, query = None):
		if query:
			self.db.vocabulary_query.drop()
			self.db.documents.map_reduce(mapFunction, reduceFunction, "temp_collection", query = query)
			self.db.eval(functionCreateQuery, query)
		else:
			self.db.vocabulary.drop()
			self.db.documents.map_reduce(mapFunction, reduceFunction, "temp_collection")
			self.db.eval(functionCreate)

	#update index after docunemts are added
	def updateIndex(self, startDate):
		query = {"createdAt": {"$gt": startDate } }
		self.db.documents.map_reduce(mapFunction, reduceFunction, "temp_collection", query = query)
		self.db.eval(functionUpdate)


	#docIDs - list of documents
	def deleteIndex(self, docIDs):
		self.db.vocabulary.update({ }, { "$pull": { "docIDs" :{ "docID": {"$in": docIDs} } }}, multi=True );
		self.db.vocabulary.remove({"docIDs" : {"$size": 0}}, multi=True )
		self.db.eval(functionDelete)