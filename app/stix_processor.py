import stix2
import datetime
from stix2validator import validate_string, print_results
import json

def jsonToStix(playbook_objs):
    current_time = datetime.datetime.now().isoformat()

    ap = stix2.AttackPattern (
    id = 'attack-pattern--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061',
    created = current_time,
    modified = current_time,
    name = "Dummy AP",
    description = "Useless"
    )

    bundle = stix2.Bundle(ap)

    newBundle = bundle

    for playbook in playbook_objs:
        newBundle.objects.append(playbook)
        del newBundle.objects[0] #delete the dummy attack pattern

    return newBundle
