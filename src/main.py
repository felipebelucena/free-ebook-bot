import requests
from bs4 import BeautifulSoup

PACKT_PUB_URL='https://www.packtpub.com/packt/offers/free-learning'

class Book(object):
    def __init__(self, name, img, description):
        self.name = name
        self.img = img
        self.description = description


def getDealOfTheDay():
    """Check in Pack Pub site what is today's ebook deal.
    """
    r = requests.get(PACKT_PUB_URL)
    ebook = Book('Dummy ebook title', 'dummy img url', 'Dummy ebook description')
    if r.status_code == 200:
        # TODO: actually parse the html and get the ebook info
        soup = BeautifulSoup(r.text, 'html.parser')
        main_div = soup.find(id='deal-of-the-day')
    
    return ebook


if __name__ == '__main__':
    ebook = getDealOfTheDay()

    print("### Free Ebook Bot tool ###")

    if ebook:
        print("Book of the day: {}".format(ebook.name))
        print("Description: {}".format( ebook.description))
    else:
        print("Sorry! There has been an error getting the deal of the day. Try again later.")
