import glob
import json
import os
import re


def aggregate():
    filepath_read = './attack-patterns/*.json'
    files = glob.glob(filepath_read)
    docs = []
    for doc in files:
        with open(doc) as f:
            data = json.load(f)
            docs.append(data)

    with open('inputdata.json', 'w+') as f:
        f.write(json.dumps(docs))

    return docs

def printj(docs):
    for doc in docs:
        print(str(doc))

def write(filepath, data):
    try:
        with open(filepath, 'w+') as f:
            f.write(json.dumps(data))
    except:
        print("Write to " + filepath + " failed.")

def strip_filename(path, length):
    return path[length:]

def process_pattern(pattern):
    valid_fields = ["name", "description", "kill_chain_phases", "external_references",
    "object_marking_refs", "created", "created_by_ref", "id", "modified", "type"]
    newpat = {}
    for key in pattern:
        if key in valid_fields:
            newpat[key] = pattern[key]

    return newpat

def transform():
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

transform()
