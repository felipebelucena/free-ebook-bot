# Free ebook bot    

Free ebook bot is simple project that gets the 'deal of the day' ebook at [PacktPub](https://www.packtpub.com/packt/offers/free-learning) and
posts on twitter.

This projects uses [requests](http://docs.python-requests.org/en/master/), [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) and [python-twitter](https://github.com/bear/python-twitter).

## How to use?

Follow [@freebookbot](https://twitter.com/freebookbot) on twitter to get the PacktPub's "deal of the day" notification.

## How to develop (or run locally on your machine)?

As python-twitter 3.x support is on development, this project uses python 2.7.11.

Read [this](https://dev.twitter.com/oauth/overview/application-owner-access-tokens) document to get the token info needed to post on your twitter account.


1. Clone the git repo.
2. Create a python 2.7.11 virtualenv and activate it.
3. Install dependencies.
4. Configure the `.env` file with your user's access token info.
5. run the app.

```console
git clone git@github.com:felipebelucena/free-ebook-bot.git free-ebook-bot
cd free-ebook-bot
virtualenv .free-ebook-bot
source .free-ebook-bot/bin/activate
pip install -r requirements.txt
cp contrib/env-sample src/.env
# edit .env file with your AccessToken/Secret and ConsumerKey/Secret info
python src/main.py --send-tweets
```

If you don't want to send tweets, run the app without the `--send-tweets` arg.