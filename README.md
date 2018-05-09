# playbookmanager
Open Source Repository for the Palo Alto Playbook Manager Application.

## Installation

If you are windows then you are on your own. Sorry :(

### Assumptions:

* You are not using windows.
* You have installed elasticsearch in a folder named `elasticsearch` in the `playbookmanager` directory.
* Using virtualenv to install all Python dependencies.
* Clone repo, install virtualenv, install python dependencies:

```
git clone https://github.com/TrevorNovak/playbookmanager`
cd playbookmanager
python3 -m virtualenv venv 
source ./venv/bin/activate 
pip install -r requirements.txt
```
Now, open up a second terminal window. In this new window:

```
cd config
make elasticsearch
```
Elasticsearch is now running locally (localhost:9200)

Once elasticsearch is setup, return to the original terminal window:

```
cd config
make index
make backend
```

Point your browser to:

http://localhost:5000
