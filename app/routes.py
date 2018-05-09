from flask import render_template, flash, redirect, url_for, jsonify, abort, request
from .attackpatterns import *
from .config import api_base_url, app_base_url, es_base_url
from app import app
from app.forms import LoginForm, AttackPatternSearchForm
from app.util import formats, extract
from app.playbook import Playbook, add_playbook, add_pattern, playbooks, playbook
from app.stix_processor import jsonToStix
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Match, Q
import pprint
import json

test_playbook = []
section = []
current_pattern = []
#attack_patterns = []


@app.route('/index')
def index():
    user = {'username': 'Trevor'}
    patterns = [
        pattern1
    ]
    playbook = []
    objects = pattern1[0]
    sections = extract(objects)
    return render_template('index.html', title='Home', user=user, sections=sections, playbook=playbook, add=add_pattern)

@app.route('/')
def root_redirect():
    return redirect(app_base_url+'create')

@app.route('/playbookmanager/create', methods=['GET', 'POST'])
def create():
    search = AttackPatternSearchForm(request.form)
    length = len(test_playbook)
    if request.method == 'POST':
        return search_results(search)

    print("Create Sections: \n")
    print(section)
    return render_template('create.html', title='Create', sections=section, playbook=test_playbook, form=search, length=length)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

# DATA LIST FOR SEARCH BAR

@app.route('/playbookmanager/api/v1/playbooks', methods=['GET'])
def get_playbooks():
    add_pattern(pattern1)
    add_pattern(pattern1)
    add_playbook(playbook)
    add_playbook(playbook)
    return jsonify({'playbooks': playbooks})
# render_template('playbook.html', title='Playbooks', playbook=playbook)

@app.route('/playbookmanager/api/v1/playbooks/<int:playbook_id>', methods=['GET'])
def getPlaybook(playbook_id):
    playbook = [playbook for playbook in playbooks if playbook['id'] == playbook_id]
    if len(playbook) == 0:
        abort(404)
    return jsonify({'playbook': playbook[0]})

@app.route('/playbookmanager/api/v1/attack-patterns', methods=['GET'])
def get_attack_patterns():
    return jsonify({'trevor': attack_patterns})

@app.route('/playbookmanager/api/v1/attack-patterns/<int:pattern_id>', methods=['GET'])
def get_attack_pattern(pattern_id):
    pattern = [pattern for pattern in attack_patterns if pattern['pid'] == pattern_id]
    if len(pattern) == 0:
        abort(404)
    return jsonify(pattern)

# @app.route('/api/v1/search', methods=['GET', 'POST'])
# def get():
#     # parse the query: ?q=[something]
#     print("IN HERE")
#     parser.add_argument('q')
#     query_string = parser.parse_args()
#     # base search URL
#     url = config.es_base_url['attack-patterns']+'/_search'
#     # Query Elasticsearch
#     query = {
#         "query": {
#             "multi_match": {
#                 "fields": ["name", "producer", "description", "styles"],
#                 "query": query_string['q'],
#                 "type": "cross_fields",
#                 "use_dis_max": False
#             }
#         },
#         "size": 100
#     }
#     resp = requests.post(url, data=json.dumps(query))
#     data = resp.json()
#     # Build an array of results
#     pattern = []
#     for hit in data['hits']['hits']:
#         pattern = hit['_source']
#         pattern['id'] = hit['_id']
#         patterns.append(pattern)
#     print("OUT THERE")
#     return jsonify(patterns)

@app.route('/api/v1/this', methods=['GET'])
def this():
    return jsonify({'this': 'example'})

@app.route('/_add_pattern')
def add_attack_pattern():
    print("Section ADD PATTERN")
    print(section)
    for c in current_pattern:
        print(c)
        test_playbook.append(c)
    section.clear()
    current_pattern.clear()
    return redirect(app_base_url+'create')

@app.route('/_remove_pattern/<int:pattern_id>')
def remove_attack_pattern(pattern_id):
    print("REMOVE ATTACK PATTERN")
    if len(test_playbook) == 0:
        print("Error. Playbook is empty.")
    else:
        print("Attack Pattern Removed: " + str(test_playbook.pop(pattern_id)))
        return redirect(app_base_url + 'create')

@app.route('/_clear_playbook')
def clear_playbook():
    test_playbook.clear()
    section.clear()
    current_pattern.clear()
    return redirect('playbookmanager/create')

@app.route('/_set_section')
def set_section(sect):
    section.append(sect)
    return redirect('playbookmanager/create')

@app.route('/_set_current')
def set_current(current):
    current_pattern.append(current)
    return redirect('playbookmanager/create')

@app.route('/_create_playbook')
def create_playbook():
    pp = pprint.PrettyPrinter(indent=4)
    if len(test_playbook) == 0:
        return redirect('playbookmanager/create')
    else:
        pp.pprint(test_playbook)
        pb = jsonToStix(test_playbook)
        pp.pprint(pb)
        pb = pb.serialize()
        # pbd = json.loads(pb)
        clear_playbook()
        return render_template('playbook.html', pb=pb)

@app.route('/playbookmanager/search', methods=['GET', 'POST'])
def do_search():
    search = AttackPatternSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('create.html', form=search)

@app.route('/results')
def search_results(search):
    section.clear()
    client = Elasticsearch()
    results = []
    #print(load_attack_patterns())
    #print("ATTACK PATTERNS")
    #print(attack_patterns)
    searchstring = search.data['search']
    print("Search String: " + searchstring)
    if searchstring:
        #pattern = search_attack_patterns(searchstring, attack_patterns)
        q = Q("match", name=searchstring)
        s = Search().using(client).query(q)
        print(s)
        response = s.execute()
        print(response)
        if not response:
            flash('No results found!')
            section.clear()
            return redirect('/playbookmanager/create')
        else:
            count = 0
            print('Total %d hits found.' % response.hits.total)
            pattern = response[0].to_dict()
            objects = pattern
            sections = extract(objects)
            set_section(sections)
            set_current(pattern)
            print(section)
            # display results
            print("Sections: \n")
            print(sections)
            return redirect('/playbookmanager/create')
    else:
        flash("You didn't enter anything.")
        section.clear()
        return redirect('/playbookmanager/create')

#Credential Dumping
    if search.data['search'] == '':
        print('Empty')
    #
    # if not results:
    # else:
    #     # display results
    #     print("Sections: \n")
    #     print(sections)
    #     return redirect('/playbookmanager/create')

"""
    client = Elasticsearch()
    results = []
    #print(load_attack_patterns())
    #print("ATTACK PATTERNS")
    #print(attack_patterns)
    searchstring = search.data['search']
    print("Search String: " + searchstring)
    if searchstring:
        #pattern = search_attack_patterns(searchstring, attack_patterns)
        q = Q("multi_match", type='cross_fields', query=searchstring, use_dis_max=False, fields=['name', 'description'])
        s = Search().using(client).query(q)
        print(s)
        response = s.execute()
        print(response)
        # if not pattern:
        #     print("ERROR")
        # else:
        for hit in s:
            print("HERE")
            print(hit.name)
            print(hit.description)


                    # for hit in response:
                    # # for hit in s:
                    #     print(hit.name)
                    #     print(hit.description)
            """

@app.route('/playbookmanager/list')
def list_pattern():
    pb = test_playbook
    return render_template('list.html', title='List', playbook=pb)

@app.route('/parse')
def parse():
    return render_template('parse.html', title='Parse')

@app.route('/test')
def test():
    return render_template('test.html')
