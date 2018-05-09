from flask import Flask
from .config import Config
from flask_restful import reqparse, Resource, Api
from flask_cors import CORS
from elasticsearch_dsl.query import MultiMatch, Match
from elasticsearch_dsl import Search
import requests
import json

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
class Search(Resource):


    def get(self):
        client = Elasticsearch()
        s = Search(using=client)
        # parse the query: ?q=[something]
        parser.add_argument('q')
        query_string = parser.parse_args()
        # base search URL
        url = config.es_base_url['attack-patterns']+'/_search'
        # Query Elasticsearch
        query = {
            "query": {
                "multi_match": {
                    "fields": ["name", "description"],
                    "query": query_string['q'],
                    "type": "cross_fields",
                    "use_dis_max": False
                }
            },
            "size": 100
        }
        resp = requests.post(url, data=json.dumps(query))
        data = resp.json()
        print(data)
        # Build an array of results
        patterns = []
        for hit in data['hits']['hits']:
            pattern = hit['_source']
            pattern['id'] = hit['_id']
            patterns.append(pattern)
        return patterns

api.add_resource(Search, config.api_base_url+'/search')

from app import routes
