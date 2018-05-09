.PHONY=help
help::
	@echo "Setup virtual environment and install requirements.txt"

.PHONY=elasticsearch
elasticsearch::
	../elasticsearch/elasticsearch-6.2.4/bin/elasticsearch -Ecluster.name=playbook_cluster -Enode.name=playbook_node

.PHONY=index
index::
	python essetup.py

.PHONY=backend
backend::
	python ../appsetup.py
	flask run
