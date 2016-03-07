from __future__ import print_function
from __future__ import unicode_literals
import requests
import twitter
import schedule
import time
import sys
from bs4 import BeautifulSoup
from decouple import config
from twitter.error import TwitterError


PACKT_PUB_URL='https://www.packtpub.com/packt/offers/free-learning'
CLASS_TITLE_DIV = 'dotd-title'
CLASS_DOTD_BOOK_SUMMARY = 'dotd-main-book-summary'
SEND_TWEETS = False

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
        text = "#DOTD: {}. {} #PacktPub".format(book.name, PACKT_PUB_URL)
        self.api.PostUpdate(text)

    def postDescription(self, book):
        text = book.description[:self.TWITTER_MAX_LENGTH]
        if len(book.description) > self.TWITTER_MAX_LENGTH:
            text = text[:-3] + '...'
        self.api.PostUpdate(text)

class Book(object):
    def __init__(self, name, description, img_url=''):
        self.name = name
        self.img_url = img_url
        self.description = description

def getTitle(soup):
    """Looks for the book title in the html parsed stored in 'soup' variable"""
    title_div = soup.find('div', class_=CLASS_TITLE_DIV)
    return title_div.h2.string.strip()

def getDescription(soup):
    """Looks for the book summary in the html parsed stored in 'soup' variable"""
    main_summary_div = soup.find(class_=CLASS_DOTD_BOOK_SUMMARY)
    # in the html page, the description items have no class or id, so I'll just look for divs with no class
    summary_div_list = main_summary_div.findAll('div', class_=lambda cssClass: cssClass == None)
    # todo: parse the <ul> tag in the second summary div and add to the description
    return summary_div_list[0].string.strip()

def getDealOfTheDay():
    """Check in Pack Pub site what today's ebook deal is.
    """
    ebook = None

    r = requests.get(PACKT_PUB_URL)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        ebook = Book(getTitle(soup), getDescription(soup))

    return ebook

def job():
    ebook = getDealOfTheDay()

    if ebook:
        print('Book of the day: {}\nDescription: {}'.format(ebook.name, ebook.description))

        if SEND_TWEETS:
            try:
                print("posting on twitter...")
                twitter = TwitterManager()
                twitter.post(ebook)
                #twitter.postDescription(ebook)
                print('Done!')
            except TwitterError as error:
                print('Error sending tweets: ', error.message)
    else:
        print('Sorry! There has been an error getting the deal of the day. Try again later.')


if __name__ == '__main__':
    print("### Free Ebook Bot tool ###")
    if len(sys.argv) > 1:
        SEND_TWEETS = sys.argv[1] == '--send-tweets'

    schedule.every(3).hours.do(job)
    # run first time
    job()

    while True:
        schedule.run_pending()
        time.sleep(1)

