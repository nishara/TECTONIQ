# coding: utf-8

__author__ = "Adrian Guille, Ciprian-Octavian Truică"
__copyright__ = "Copyright 2015, University Politehnica of Bucharest"
__license__ = "GNU GPL"
__version__ = "0.1"
__email__ = "[ciprian.truica@cs.pub.ro, ]"
__status__ = "Production"


from flask import Flask, Response, render_template, request
from indexing.vocabulary_index import VocabularyIndex
from search_mongo import Search
import pymongo

client = pymongo.MongoClient()
db = client['Tectoniq']

app = Flask(__name__)

@app.route('/tectoniq/analysis')
def analysis_dashboard_page(name=None):
    return render_template('analysis.html', name=name) 

@app.route('/tectoniq/analysis',methods=['POST'])
def getDocuments():
    query = request.form['cooccurringwords']
    search = Search(query)
    results = search.results()
    csv = 'author,timestamp,text,score\n'
    html = """  
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.7/css/jquery.dataTables.css">
        <style type="text/css" class="init"></style>
        <script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-1.11.1.min.js"></script>
    	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
        <script type="text/javascript" class="init">
            $(document).ready(function() {
    	        $('#example').DataTable();
            } );
        </script>
    </head>
    <body>
        <table id="example" class="display" cellspacing="0" width="100%">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Score</th>
                </tr>
            </thead>
            <tbody>
    """
    for doc in results :
        html += "<tr><td>"+str(doc['recordId'])+'</td><td>'+str(doc['title'])+'</td><td>'+doc['description']+'</td><td>'+str(doc['score'])+'</td></tr>'
        
    html += "</tbody></table></body></html>"
    #return Response(csv,mimetype="text/csv")
    return html
    
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
