import urllib2
from urlparse import urlparse

from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect

from forms import *
from models import *
from html_parser import parser


def login_user(request, template="templates/login.html"):
    context = {}

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                return render_to_response(template, {}, context_instance=RequestContext(request))
        else:
            pass

    context['form'] = LoginForm()
    return render_to_response(template, context, context_instance=RequestContext(request))

def logout_user(request):
    context = {}
    logout(request)
    return redirect('login')

@login_required
def home(request, template="templates/index.html"):
    context = {'username': request.user.username}
    user = request.user
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def cards(request, template="templates/cards.html"):
    context = {}

    if request.method == "POST":
        if request.POST.has_key('card_name'):
            card_name = request.POST['card_name']

            card = Card.objects.filter(card_name=card_name)

            if len(card) == 0:
                card = Card()
                card.card_name = card_name

                _parser = parser(card_name)
                html_obj = urllib2.urlopen("http://magiccards.info/query?q=%s" % card_name.replace(' ', '+').replace(',', '%2C'))
                html_text = html_obj.read()
                html_text = html_text.decode('utf-8')
                _parser.feed(html_text)
                
                img_url = _parser.url
                filename = urlparse(img_url).path.split('/')[-1]
            
                content = ContentFile(urllib2.urlopen(img_url).read())
                card.image.save("%s.jpg" % card_name, content, save=True)
                
                
            else:
                card = card[0]

        else:
            deck = Deck.objects.create(name=request.POST['deck_name'])
            for i in request.POST.keys():
                if i[:5] == "card_" and request.POST[i] != '':
                    card = Card.objects.get(card_name=i[5:])
                    decked_card = DeckCard.objects.create(deck=deck, card=card, quantity=int(request.POST[i]))

        featured_card = card.image
        context['featured_card'] = featured_card
                    
    cards = Card.objects.all()
    context['cards'] = cards

    if len(cards) > 0 and not context.has_key('featured_card'):
        featured_card = cards[0].image
        context['featured_card'] = featured_card

    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def deck(request, template="templates/game.html"):
    context = {}

    decks = Deck.objects.all()
    deck_choice_form = DeckChoiceForm()
    context['deck_choice_form'] = deck_choice_form

    if len(decks) > 0:
        context['decks'] = decks

    if request.method == "POST" and request.POST['deck'] != None:
        deck = Deck.objects.get(pk=request.POST['deck'])
        deck.is_active = True
        deck.save()

        return redirect('game')

    return render_to_response("templates/deck.html",
                              context,
                              context_instance=RequestContext(request))


@login_required
def game(request, template="templates/game.html"):
    context = {}

    deck = Deck.objects.get(is_active=True)

    cards = []

    from random import shuffle

    deckcards = set(DeckCard.objects.filter(deck=deck))
    deckcards = list(deckcards)

    for card in deckcards:
        cards += [card] * card.quantity

    shuffle(cards)
    context['cards'] = cards
#        cache.set('library', cards[:], 1000)
#        cache.set('hand', cards[:6], 1000)
    context['library'] = cards[:]
    context['hand'] = cards[:6]
    context['back_of_card'] = Card.objects.get(card_name='back_of_card').image

    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))
