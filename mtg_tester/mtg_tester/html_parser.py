from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class parser(HTMLParser):
    def __init__(self, card_name):
        HTMLParser.__init__(self)
        self.url = None
        self.card_name = card_name

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for attr in attrs:
                if attrs[1][0] == "alt" and attrs[1][1].lower() == str(self.card_name.lower()) and "scans" in attr[1]:
                    self.url = attr[1]
