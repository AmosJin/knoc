from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http.response import HttpResponseRedirect, reverse

from post.models import Item, Link, Note, Group, UserGroup
from post import core
from post.forms import NoteForm, LinkForm


@login_required
def home(request, group_name=None):
    if not group_name:
        default_group = Group.objects.get(pk=1)
    
    return render('posts/templates/items.html', 


@login_required
def create_note(request, group_id):
    user = request.user
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        raise Http404

    form = NoteForm(request.POST)
    if form.is_valid():
        note = form.save()
        item = core.update_item(note, user_id=user.pk, group_id=group.pk)
        return 

    
    
    

