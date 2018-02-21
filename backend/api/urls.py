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
from api import views

urlpatterns = [
    url(r'^$', generic.RedirectView.as_view(
         url='/api/', permanent=False)),
    url(r'^api/v1/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/auth/token/obtain/$', TokenObtainPairView.as_view()),
    url(r'^api/v1/auth/token/refresh/$', TokenRefreshView.as_view()),
    url(r'^api/v1/echo/$', views.EchoView.as_view()),
    url(r'^api/v1/playbooks/$', views.PlaybookList.as_view()),
    url(r'^api/v1/playbooks/(?P<pk>[0-9]+)$', views.PlaybookDetail.as_view()),
    url(r'^api/v1/users/$', views.UserList.as_view()),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    # url(r'^api/v1/schema/$', views.schema_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)
