from django.conf.urls import url
from django.views import generic
from django.conf.urls import url, include
from django.views import generic
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authtoken import views as drf_views
from rest_framework import views, serializers, status
from rest_framework.urlpatterns import format_suffix_patterns
from api.serializers import MessageSerializer, PlaybookSerializer
from api import views

urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(
         url='/api/', permanent=False)),
    url(r'^api/$', get_schema_view()),
    url(r'^api/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^api/auth/token/refresh/$', TokenRefreshView.as_view()),
    url(r'^api/echo/$', views.EchoView.as_view()),
    url(r'^api/playbooks/$', views.PlaybookList.as_view()),
    url(r'^api/playbooks/(?P<pk>[0-9]+)$', views.PlaybookDetail.as_view()),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
