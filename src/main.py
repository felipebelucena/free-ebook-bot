from __future__ import print_function, unicode_literals
from bs4 import BeautifulSoup
from decouple import config
import twitter
import requests
import sys


PACKT_PUB_URL='https://www.packtpub.com/packt/offers/free-learning'
CLASS_TITLE_DIV = 'dotd-title'
CLASS_DOTD_BOOK_SUMMARY = 'dotd-main-book-summary'
NO_TWEETS = False

class TwitterManager(object):
    CONSUMER_KEY = config('CONSUMER_KEY')
    CONSUMER_SECRET = config('CONSUMER_SECRET')
    ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')
    ACCESS_TOKEN_KEY = config('ACCESS_TOKEN')
    TWITTER_MAX_LENGTH = 140

    def __init__(self):
        self.api = twitter.Api(consumer_key=self.CONSUMER_KEY,
                       consumer_secret=self.CONSUMER_SECRET,
                       access_token_key=self.ACCESS_TOKEN_KEY,
                       access_token_secret=self.ACCESS_TOKEN_SECRET)

    def post(self, book):
        text = "#DOTD: {}. {} #PacktPub".format(book, PACKT_PUB_URL)
        self.api.PostUpdate(text)

    def post_description(self, book):
        text = book.description[:self.TWITTER_MAX_LENGTH]
        if len(book.description) > self.TWITTER_MAX_LENGTH:
            text = text[:-3] + '...'
        self.api.PostUpdate(text)

class Book(object):
    def __init__(self, name, description, img_url=''):
        self.name = name
        self.img_url = img_url
        self.description = description

    def __str__(self):
        return self.name


def get_title(soup):
    """Looks for the book title in the html parsed stored in 'soup' variable"""
    title_div = soup.find('div', class_=CLASS_TITLE_DIV)
    return unicode(title_div.h2.string.strip())

def get_description(soup):
    """Looks for the book summary in the html parsed stored in 'soup' variable"""
    main_summary_div = soup.find(class_=CLASS_DOTD_BOOK_SUMMARY)
    # in the html page, the description items have no class or id, so I'll just look for divs with no class
    summary_div_list = main_summary_div.findAll('div', class_=lambda cssClass: cssClass == None)
    # todo: parse the <ul> tag in the second summary div and add to the description
    return unicode(summary_div_list[0].string.strip())

def get_dotd():
    """Check in Pack Pub site what the 'deal of the day (dotd)' is.
    """
    r = requests.get(PACKT_PUB_URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        ebook = Book(get_title(soup), get_description(soup))

        print('Book of the day: ', ebook)
        print('Description: ', ebook.description)

        if NO_TWEETS:
            return
        try:
            print("posting on twitter...")
            tm = TwitterManager()
            tm.post(ebook)
            print('Done!')
        except twitter.error.TwitterError as error:
            print('Error sending tweet:')
            for msg in error.message:
                print('[{}] - {}'.format(msg['code'],  msg['message']))
    else:
        print('Sorry! There has been an error getting the deal of the day. Try again later.')


if __name__ == '__main__':
    print("### Free Ebook Bot tool ###")
    if len(sys.argv) > 1:
        NO_TWEETS = sys.argv[1] == '--no-tweet'

    get_dotd()
