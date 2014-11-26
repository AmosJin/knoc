from django.forms import ModelForm
from post.models import Link, Note

class LinkForm(ModelForm):
    class Meta:
        model = Link


class NoteForm(ModelForm):
    class Meta:
        model = Note
