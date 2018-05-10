import stix2
import datetime
from stix2validator import validate_string, print_results
import json

def dictToStix(playbook):

    if len(playbook) > 0:
        bundle = stix2.Bundle(playbook[0])
        for pattern in playbook:
            bundle.objects.append(pattern)

        return bundle

def validator(pattern):
    pass
