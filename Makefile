.PHONY=help
help::
	@echo "Setup virtual environment and install requirements.txt"

.PHONY=backend
backend::
	python setup.py
	export FLASK_APP=playbookmanager.py
	export FLASK_ENV=development
	flask run
