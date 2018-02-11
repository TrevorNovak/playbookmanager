from api.models import Playbook
from api.serializers import PlaybookSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PlaybookList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        playbooks = Playbook.objects.all()
        serializer = PlaybookSerializer(playbooks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlaybookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaybookDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            playbook = Playbook.objects.get(pk=pk)
        except Playbook.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        playbook = self.get_object(pk)
        serializer = PlaybookSerializer(playbook)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        playbook = self.get_object(pk)
        serializer = PlaybookSerializer(playbook, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        playbook = self.get_object(pk)
        playbook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
