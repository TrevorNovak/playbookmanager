import glob
import json
import os
import re

"""
This file contains a set of utility functions used to aggregate and transform
attack patterns. The reason for this is that the STIX bundler can only process
certain fields, and Elasticsearch has an easier time indexing flat dictionaries,
so removing the contents of the objects array greatly simplifies this process.
"""

def aggregate():
    """
    This function aggregates all .json files located in filepath_read into
    file. Also appends them into a list. Can be used to assist in bulk indexing
    done through curl.

    returns list of dictionaries representing each .json file.
    """
    filepath_read = './attack-patterns/*.json'
    files = glob.glob(filepath_read)
    docs = []
    for doc in files:
        with open(doc) as f:
            data = json.load(f)
            docs.append(data)

    for doc in docs:
        write('inputdata.json', doc)

    return docs

def write(filepath, data):
    """
    Writes given data to the given filepath. Used by aggregate() and transform().
    """
    try:
        with open(filepath, 'w+') as f:
            f.write(json.dumps(data))
    except:
        print("Write to " + filepath + " failed.")

def transform():
    """
    Used to transform attack patterns into modified .json documents that allows for easier
    indexing, storage, and retrieval. Extracts contents of objects array, and removes
    key-value pairs that the stix bundler cannot handle. Leaves original attack patterns
    in tact, unmodified.
    """
    filepath = './attack-patterns/'
    filepath_read = './attack-patterns/*.json'
    filepath_write = './modified-attack-patterns/'
    files = glob.glob(filepath_read)
    count = 0
    data = []
    newpattern = {}

    for doc in files:
        with open(doc) as f:
            data = json.load(f)
            try:
                newpattern = data.pop('objects')[0]
                newpattern = process_pattern(newpattern)
                docname = strip_filename(doc, len(filepath))
                write(filepath_write+docname, newpattern)
                count = count + 1
            except:
                print("Object list extraction failed on " + doc)

    print("The script read in " + str(len(files)) + " files. The script processed and wrote to " + str(count) + " files.")

def process_pattern(pattern):
    """
    Called by transform() to remove any invalid key-value pairs that the stix bundler
    unable to process.

    returns the new attack pattern in dictionary form
    """
    valid_fields = ["name", "description", "kill_chain_phases", "external_references",
    "object_marking_refs", "created", "created_by_ref", "id", "modified", "type"]
    newpat = {}
    for key in pattern:
        if key in valid_fields:
            newpat[key] = pattern[key]

    return newpat

def strip_filename(path, length):
    return path[length:]

def printj(docs):
    for doc in docs:
        print(str(doc))
