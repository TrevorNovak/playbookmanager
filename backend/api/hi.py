from api.models import Playbook
from api.serializers import PlaybookSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

playbook = Playbook(title='new title', body='new body baby')
playbook.save()
serializer = PlaybookSerializer(playbook)
content = JSONRenderer().render(serializer.data)

playbook = Playbook(title='qwies title', body='nesaSy baby')
playbook.save()
serializer = PlaybookSerializer(playbook)
content = JSONRenderer().render(serializer.data)
