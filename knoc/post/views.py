from django.shortcuts import render_to_response as render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader

from post.models import Item, Link, Note, Group, UserGroup
from post import core
from post.forms import NoteForm, LinkForm


@login_required
def home(request):
    context = RequestContext(request, {"request": request})
    return render('post/home.html', context)


