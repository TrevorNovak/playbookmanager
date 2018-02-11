from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path

urlpatterns = [
     url(r'^', include('api.urls')),
     path('admin/', admin.site.urls),
]
