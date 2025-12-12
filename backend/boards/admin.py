from django.contrib import admin
from .models import Workspace, Board, List, Card

admin.site.register(Workspace)
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Card)