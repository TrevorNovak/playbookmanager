import glob
import json
import os

def load_attack_patterns():
    attack_pat = []
    filepath_read = './static/modified-attack-patterns/*.json'
    files = glob.glob(filepath_read)
    print("Loaded attack patterns...")
    for doc in files:
        with open(doc) as f:
            data = json.load(f)
            try:
                attack_pat.append(data)
            except:
                print("Could not append." + doc)

    print(attack_pat)
    return attack_pat

def get_search_pattern(attack_patterns):
    for pattern in attack_patterns:
        print(pattern['name'])

def search_attack_patterns(search_string, attack_patterns):
    search_str = search_string.lower()
    if not search_str:
        return ""
    for pattern in attack_patterns:
        name = pattern['name'].lower()
        if name == search_str:
            return pattern
    return None
