from api.models import Playbook
from api.serializers import PlaybookSerializer, UserSerializer
from rest_framework import generics, views, permissions
from api.permissions import IsOwnerOrReadOnly
from api.serializers import MessageSerializer, PlaybookSerializer

from django.contrib.auth.models import User

##### TEMPLATE VIEWS ########

def detail(request, playbook_id):
    return HttpResponse("You're looking at playbook %s." % playbook_id)

def results(request, playbook_id):
    response = "You're looking at a list of playbooks %s."
    return HttpResponse(response % playbook_id)


##### REST API VIEWS ########
class UserList(generics.ListAPIView):
    """
    Returns a list of Users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Returns a user profile.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PlaybookList(generics.ListCreateAPIView):
    """
    Create and get a list of Playbooks.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Playbook.objects.all()
    serializer_class = PlaybookSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PlaybookDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Create, edit, view an individual Playbook.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)
    queryset = Playbook.objects.all()
    serializer_class = PlaybookSerializer

class EchoView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)
