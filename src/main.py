import requests
from bs4 import BeautifulSoup


PACKT_PUB_URL='https://www.packtpub.com/packt/offers/free-learning'
CLASS_TITLE_DIV = 'dotd-title'
CLASS_DOTD_BOOK_SUMMARY = 'dotd-main-book-summary'

class Book(object):
    def __init__(self, name, img, description):
        self.name = name
        self.img = img
        self.description = description

def getTitle(soup):
    title_div = soup.find('div', class_=CLASS_TITLE_DIV)
    return title_div.h2.string.strip()

def getDescription(soup):
    main_summary_div = soup.find(class_=CLASS_DOTD_BOOK_SUMMARY)
    # in the html page, the description items have no class or id, so I'll just look for divs with no class
    summary_div_list = main_summary_div.findAll('div', class_=lambda cssClass: cssClass == None)
    # todo: parse the <ul> tag in the second summary div and add to the description
    return summary_div_list[0].string.strip()

def getDealOfTheDay():
    """Check in Pack Pub site what today's ebook deal is.
    """
    r = requests.get(PACKT_PUB_URL)
    ebook = Book('Dummy ebook title', 'dummy img url', 'Dummy ebook description')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        ebook.name = getTitle(soup)
        ebook.description = getDescription(soup)

    return ebook


if __name__ == '__main__':
    ebook = getDealOfTheDay()

    print("### Free Ebook Bot tool ###")

    if ebook:
        print("Book of the day: {}".format(ebook.name))
        print("Description: {}".format( ebook.description))
    else:
        print("Sorry! There has been an error getting the deal of the day. Try again later.")
