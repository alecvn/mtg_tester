from django.forms import *

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from models import *


class LoginForm(Form):

    username = CharField(required=True, label="Username")
    password = CharField(widget=PasswordInput, required=True, label="Password")


class DeckChoiceForm(Form):
    deck = ModelChoiceField(queryset=Deck.objects.all())


class CreateDeckForm(ModelForm):

    class Meta:
        model = Deck
        fields = ['name', 'user', 'cards']
