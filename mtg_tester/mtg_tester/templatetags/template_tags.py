from django import template
#from helpers.sessions import get_all_logged_in_users
register = template.Library()

# @register.inclusion_tag('logged_in_user_list.html')
# def render_logged_in_user_list():
#     return { 'users': get_all_logged_in_users() }

@register.inclusion_tag('card_context.html')
def render_card_context(card, counter):
    return {'card': card,
            'counter': counter}
