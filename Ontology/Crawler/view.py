__author__ = 'Nishara'

from flask import Flask, render_template, request
from flask import jsonify
import rdflib

# An instance of this class will be the WSGI application
app = Flask(__name__)

# Route() decorator to tell Flask what URL should trigger our function.
@app.route('/')
def index(name=None):
    return render_template('test1.html', name=name)

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/result')
def getResults():
    # query = request.form['keyword']
    rdf = "output.owl"
    g = rdflib.Graph()
    g.parse(rdf)
    # qry = "PREFIX tectoniq: <http://www.semanticweb.org/nishara/ontologies/2015/4/tectoniq#> " \
    #         "SELECT ?name ?description WHERE {{?name tectoniq:hasDescription ?description }}"

    qry = "PREFIX tectoniq: <http://www.semanticweb.org/nishara/ontologies/2015/4/tectoniq#> " \
            "SELECT DISTINCT ?image ?period ?epoch	" \
            "WHERE	{ ?image tectoniq:belongsToPeriod ?period." \
            "?period tectoniq:hasEpoch ?epoch }"
    r = g.query(qry)
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
                    <th>Image_ID</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
    """
    for doc in r :
        html += "<tr><td>"+str(doc[0].split('#')[-1])+'</td><td>'+str(doc[1])+'</td></tr>'

    html += "</tbody></table></body></html>"
    return html


if __name__ == "__main__":
    app.debug = True
    app.run()


