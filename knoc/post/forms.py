from django.forms import ModelForm
from post.models import Link, Note

class LinkURLForm(ModelForm):
    class Meta:
        model = Link
        field =('link', ) 

class LinkForm(ModelForm):
    class Meta:
        model = Link

class NoteForm(ModelForm):
    class Meta:
        model = Note
