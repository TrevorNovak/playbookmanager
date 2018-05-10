import os
import glob
import json
from elasticsearch_dsl.connections import connections
import elasticsearch_dsl as dsl
from elasticsearch_dsl import analyzer, tokenizer, Index, DocType, Text, Date, Search, MultiSearch
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

connections.create_connection()

"""
This file is primarily responsible for defining and indexing documents
(e.g. attack patterns and playbooks)
"""

class AttackPatternIndex(DocType):
    """
    This class defines the Attack Pattern Index and associated mappings by
    inheriting from the elasticsearch-dsl DocType.
    """
    name = Text()
    description = Text()
    created = Text()
    created_by_ref = Text()
    pid = Text()
    modified = Text()
    ptype = Text()

    class Meta:
        index = 'attack-patterns'

def indexing(pattern, count):
    """
    This function takes a given attack pattern and maps its values to the
    object fields used to represent this attack pattern.
    """
    obj = AttackPatternIndex(
        meta={'id': count},
        name = pattern['name'],
        description = pattern['description'],
        kill_chain_phases = pattern['kill_chain_phases'],
        external_references = pattern['external_references'],
        object_marking_refs = pattern['object_marking_refs'],
        created = pattern['created'],
        created_by_ref = pattern['created_by_ref'],
        id = pattern['id'],
        modified = pattern['modified'],
        type = pattern['type']
    )
    obj.save()
    return obj.to_dict(include_meta=True)

def load_attack_patterns():
    """
    Reads in the modified attack patterns and stores them in a list as a member
    of a pair. The attack pattern dictionary is the first member of the pair
    and its desired index number is the second member of the tuple.

    returns the list of pairs -> (attack_pattern, id)
    """
    attack_pat = []
    count = 0
    filepath_read = 'modified-attack-patterns/*.json'
    files = glob.glob(filepath_read)
    print("Loading attack patterns...")
    for doc in files:
        with open(doc) as f:
            data = json.load(f)
            try:
                attack_pat.append((data, count))
                count += 1
            except:
                print("Could not append." + doc)
    return attack_pat

def bulk_indexing():
    """
    This function is responsible for bulk indexing the attack patterns. First,
    we declare an edge_ngram_analyzer which is the primary driver for 'Search As You Type'.

    Next we define the attack-pattern index that we want to create (e.g. settings, doc type, analyzer).
    Then, we load the attack pattern/index pair list generated from load_attack_patterns() and use
    the elasticsearch-dsl bulk indexing function to do the heavy lifting.
    """
    edge_ngram_analyzer = dsl.analyzer(
        'edge_ngram_analyzer',
        type='custom',
        tokenizer='standard',
        filter=[
            'lowercase',
            dsl.token_filter(
                'edge_ngram_filter', type='edgeNGram',
                min_gram=1, max_gram=20
            )
        ]
    )

    try:
        ap_index = Index('attack-patterns')
        ap_index.settings(number_of_shards=1)
        ap_index.doc_type(AttackPatternIndex)
        ap_index.analyzer(edge_ngram_analyzer)
        ap_index.create()
        es = Elasticsearch()
        attack_patterns = load_attack_patterns()
        print(attack_patterns)
        #p[0] is the attack pattern dictionary and p[1] is the index number.
        bulk(client=es, actions=(indexing(p[0], p[1]) for p in attack_patterns))
        print("Index successfully created and bulk indexing has completed.")
    except:
        print("Bulk Indexing has failed...")

def search_pattern(name):
    s = Search().filter('term', name=name)
    response = s.execute()
    return response
