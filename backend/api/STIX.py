import stix2
from stix2validator import validate_string, print_results

class Attack_Pattern:

	def __init__(self, id, ref , name, description):
		self.id = id
		self.ref = ref
		self.name = name
		self.description = description


def create_stix(instance):
	list_of_objects = []

	ID = instance.title
	ref = None
	name = instance.owner
	description = instance.body

	attack = Attack_Pattern(ID, ref, name, description)

	ap = stix2.AttackPattern (
		id = instance.id, # Must start with "attack-pattern--"
		created = instance.created_at,
		modified = instance.updated_at,
		name = attack.name,
		description = attack.description
		)

	list_of_objects.append(ap)

	bundle = stix2.Bundle(objects=list_of_objects)

	return bundle

	#attack-pattern--0c7b5b88-8ff7-4a4d-aa9d-feb398cd0061