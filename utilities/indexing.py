import os
import glob
import json
from elasticsearch_dsl.connections import connections
import elasticsearch_dsl as dsl
from elasticsearch_dsl import analyzer, tokenizer, Index, DocType, Text, Date, Search, MultiSearch
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

connections.create_connection()

class AttackPatternIndex(DocType):
    name = Text()
    description = Text()
    # kill_chain_phases = None
    # external_references = dsl.Nested()
    # object_marking_refs = dsl.Nested()
    created = Text()
    created_by_ref = Text()
    pid = Text()
    modified = Text()
    ptype = Text()

    class Meta:
        index = 'attack-patterns'

def indexing(pattern, count):
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
    attack_pat = []
    count = 0
    filepath_read = './modified-attack-patterns/*.json'
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

def bulk_indexing():
    ap_index = Index('attack-patterns')
    ap_index.settings(number_of_shards=1)
    ap_index.doc_type(AttackPatternIndex)
    ap_index.analyzer(edge_ngram_analyzer)
    ap_index.create()
    #AttackPatternIndex.init(index='attack-pattern')
    #index.analyzer(analyzer('default', tokenizer='standard', filter=['english...']))
    es = Elasticsearch()
    attack_patterns = load_attack_patterns()
    bulk(client=es, actions=(indexing(p[0], p[1]) for p in attack_patterns))
    print("Success")

def search_pattern(name):
    s = Search().filter('term', name=name)
    response = s.execute()
    return response

#bulk_indexing()

"""
["name", "description", "kill_chain_phases", "external_references",
"object_marking_refs", "created", "created_by_ref", "id", "modified", "type"]
{
    "name": "Execution through Module Load",
    "description": "The Windows module loader can be instructed to load DLLs from arbitrary local paths and arbitrary Universal Naming Convention (UNC) network paths. This functionality resides in NTDLL.dll and is part of the Windows Native API which is called from functions like CreateProcess(), LoadLibrary(), etc. of the Win32 API. (Citation: Wikipedia Windows Library Files)\n\nThe module loader can load DLLs:\n\n*via specification of the (fully-qualified or relative) DLL pathname in the IMPORT directory;\n    \n*via EXPORT forwarded to another DLL, specified with (fully-qualified or relative) pathname (but without extension);\n    \n*via an NTFS junction or symlink program.exe.local with the fully-qualified or relative pathname of a directory containing the DLLs specified in the IMPORT directory or forwarded EXPORTs;\n    \n*via <code><file name=\"filename.extension\" loadFrom=\"fully-qualified or relative pathname\"></code> in an embedded or external \"application manifest\". The file name refers to an entry in the IMPORT directory or a forwarded EXPORT.\n\nAdversaries can use this functionality as a way to execute arbitrary code on a system.\n\nDetection: Monitoring DLL module loads may generate a significant amount of data and may not be directly useful for defense unless collected under specific circumstances, since benign use of Windows modules load functions are common and may be difficult to distinguish from malicious behavior. Legitimate software will likely only need to load routine, bundled DLL modules or Windows system DLLs such that deviation from known module loads may be suspicious. Limiting DLL module loads to <code>%SystemRoot%</code> and <code>%ProgramFiles%</code> directories will protect against module loads from unsafe paths. \n\nCorrelation of other events with behavior surrounding module loads using API monitoring and suspicious DLLs written to disk will provide additional context to an event that may assist in determining if it is due to malicious behavior.\n\nPlatforms: Windows\n\nData Sources: Process Monitoring, API monitoring, File monitoring, DLL monitoring\n\nPermissions Required: User\n\nContributors: Stefan Kanthak",
    "kill_chain_phases": [{"kill_chain_name": "mitre-attack", "phase_name": "execution"}],
    "external_references": [{"url": "https://attack.mitre.org/wiki/Technique/T1129", "source_name": "mitre-attack", "external_id": "T1129"}, {"description": "Wikipedia. (2017, January 31). Microsoft Windows library files. Retrieved February 13, 2017.", "source_name": "Wikipedia Windows Library Files", "url": "https://en.wikipedia.org/wiki/Microsoft%20Windows%20library%20files"}],
    "object_marking_refs": ["marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"],
    "created": "2017-05-31T21:31:40.542Z",
    "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
    "id": "attack-pattern--0a5231ec-41af-4a35-83d0-6bdf11f28c65",
    "modified": "2018-04-18T17:59:24.739Z",
    "type": "attack-pattern"
}
"""
