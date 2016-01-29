from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.ext.cors import CORS
from tulip import *
from tulipgui import *
import tulippaths as tp


app = Flask(__name__)
api = Api(app)
CORS(app)
import json
parser = reqparse.RequestParser()
parser.add_argument('graph')
parser.add_argument('path')
graphFileDictionary = {
    'one': '../data/test_one.tlp',
    'feedback': '../data/test_feedback.tlp',
    'full': '../data/514_10hops_22Jan16.tlp'
}

class GraphResource(Resource):

    def get(self):
        args = parser.parse_args()
        filename = graphFileDictionary[args['graph']]
        graph = tlp.loadGraph(filename)
        print tp.export.graphToJson(graph)
        return tp.export.graphToJson(graph)


class MatrixResource(Resource):
    def get(self):
        args = parser.parse_args()
        inputQuery = json.loads(args['path'])
        filename = graphFileDictionary[args['graph']]
        query = {}

        # Convert from unicode to ascii. Will this work on non-windows machines?
        for key in inputQuery.keys():
            newValues = []
            for value in inputQuery[key]:
                newValues.append(str(value))
            query[str(key)] = newValues


        graph = tlp.loadGraph(filename)
        print json.dumps(tp.export.graphToJson(graph))
        matrix = tp.ConnectivityMatrix(graph)

        matrix.activate(query['nodeConstraints'], query['edgeConstraints'])
        return matrix.getAsJsonObject()

api.add_resource(GraphResource, '/')
api.add_resource(MatrixResource, '/matrix')

if __name__ == '__main__':
    app.run(debug=True)