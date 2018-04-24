from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Text, Date, Search
from . import models

connections.create_connection()

class PlaybookIndex(DocType):
    created = Date()
    title = Text()
    body = Text()
    owner = Text()

    class Meta:
        index = 'playbook-index'

def bulk_indexing():
    PlaybookIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(p.indexing() for p in models.Playbook.objects.all().iterator()))

def search(author):
    s = Search().filter('term', owner=author)
    response = s.execute()
    return response
