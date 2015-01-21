from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
import settings


class Card(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    card_name = models.TextField(null=True, blank=True)

class Deck(models.Model):
    cards = models.ManyToManyField(Card, through="DeckCard", null=True)
    name = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, db_index=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)
    quantity = models.IntegerField()
