import json

playbooks = []

playbook = []

def add_playbook(playbook):
    playbooks.append(playbook)

def add_pattern(pattern):
    playbook.append(pattern)

class Playbook():

    def __init__(self):
        self.playbook = []
        self.id = 0

    def set_id(self, id):
        self.id = id

    def add_pattern(self, pattern):
        self.playbook.append(pattern)

    def get_playbook(self):
        return self.playbook

    def clear_playbook(self):
        self.playbook = []
