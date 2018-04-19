from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Playbook

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()

class PlaybookSerializer(serializers.Serializer):
    """
    The Playbook serializer serializes the Playbook model into JSON.
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    body = serializers.CharField(style={'base_template': 'textarea.html'})

    class Meta:
        model = Playbook
        fields = ('id', 'title', 'body')
        owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Playbook.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    """
    The Playbook serializer serializes the Playbook model into JSON.
    """
    playbooks = serializers.PrimaryKeyRelatedField(many=True, queryset=Playbook.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'playbooks')
