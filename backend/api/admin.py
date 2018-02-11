from django.contrib import admin
from api.models import Playbook

class PlaybookAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list.html'
    list_display = [ 'title', 'body', ]

admin.site.register(Playbook, PlaybookAdmin)
