from flask import render_template, flash, redirect, url_for, jsonify, abort, request

from app import app
from app.attackpatterns import *
from app.config import api_base_url, app_base_url, es_base_url
from app.forms import LoginForm, AttackPatternSearchForm
from app.util import formats, extract
from app.playbook import Playbook, add_playbook, add_pattern, playbooks, playbook
from app.stix_processor import dictToStix
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Match, Q
import pprint
import json

playbook = []
section = []
current_pattern = []
#attack_patterns = []

"""
Defines the routes and views used within the application. Work in progress, excuse the mess.
"""

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
    length = len(playbook)
    if request.method == 'POST':
        return search_results(search)

    print("Create Sections: \n")
    print(section)
    return render_template('create.html', title='Create', sections=section, playbook=playbook, form=search, length=length)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/playbookmanager/api/v1/playbooks', methods=['GET'])
def get_playbooks():
    add_pattern(pattern1)
    add_pattern(pattern1)
    add_playbook(playbook)
    add_playbook(playbook)
    return jsonify({'playbooks': playbooks})

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

@app.route('/api/v1/this', methods=['GET'])
def this():
    return jsonify({'this': 'example'})

@app.route('/_add_pattern')
def add_attack_pattern():
    print("Section ADD PATTERN")
    print(section)
    for c in current_pattern:
        print(c)
        playbook.append(c)
    section.clear()
    current_pattern.clear()
    return redirect(app_base_url+'create')

@app.route('/_remove_pattern/<int:pattern_id>')
def remove_attack_pattern(pattern_id):
    print("REMOVE ATTACK PATTERN")
    if len(playbook) == 0:
        print("Error. Playbook is empty.")
    else:
        print("Attack Pattern Removed: " + str(playbook.pop(pattern_id)))
        return redirect(app_base_url + 'create')

@app.route('/_clear_playbook')
def clear_playbook():
    playbook.clear()
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
    if len(playbook) == 0:
        return redirect('playbookmanager/create')
    else:
        pp.pprint(playbook)
        pb = dictToStix(playbook)
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

    searchstring = search.data['search']
    print("Search String: " + searchstring)
    if searchstring:
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

    if search.data['search'] == '':
        print('Empty')

@app.route('/playbookmanager/list')
def list_pattern():
    pb = playbook
    return render_template('list.html', title='List', playbook=pb)

@app.route('/parse')
def parse():
    return render_template('parse.html', title='Parse')

@app.route('/test')
def test():
    return render_template('test.html')
