from django.contrib import admin
from post.models import Group, UserGroup, Link, Note, Item

for model in Group, UserGroup, Link, Note, Item:
    admin.site.register(model)
