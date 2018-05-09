import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'insert-backup-secret-key-here'

api_base_url = '/api/v1'
app_base_url = 'playbookmanager/'
es_base_url = {
    'attack-patterns': 'http://localhost:9200/attack-patterns/doc',
    'playbooks': 'http://localhost:9200/playbooks/doc',
}
