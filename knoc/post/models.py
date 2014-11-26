from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from taggit.managers import TaggableManager

class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UserGroup(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    def __str__(self):
        return "{user_group.user.username}-{user_group.group.name}".format(user_group=self)

class Link(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField(default="")
    link = models.URLField()
    image = models.URLField(default="")

    def __str__(self):
        return self.title

    @property
    def item_type(self):
        return "link"

class Note(models.Model):
    title = models.CharField(max_length=1024)
    summary = models.CharField(max_length=1024)
    content = models.TextField(default="")

    def __str__(self):
        return self.title

    @property
    def item_type(self):
        return "note"

class Item(models.Model):
    group = models.ForeignKey(Group)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    item = generic.GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True, related_name="item_tags")

    @property
    def item_type(self):
        return self.item.item_type

    @property
    def author_info(self):
        author = self.author
        return {
                "id": author.pk,
                "username": author.username
                }

    @property
    def tag_list(self):
        return self.tags.names()

    class Meta:
        unique_together = ('content_type','object_id')

    class Manifest:
        excludes = ("content_type","author_id")
        properties = ("item_type", "tag_list", "author_info")

    def __str__(self):
        return self.item.title

