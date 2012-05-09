import os
import json
from flask import Flask, g, session, jsonify
from flask import render_template, redirect, url_for, request
from flask.ext.celery import Celery
from gevent.pywsgi import WSGIServer
from juggernaut import Juggernaut

from models import TwitterItem

def create_app():
    return Flask(__name__)

app = create_app()
app.debug = True
app.config.from_pyfile("config.py")

jug = Juggernaut()
celery = Celery(app)

@celery.task(name="sonar.update")
def update():
    update_tweets()

def update_tweets():
    tweets = TwitterItem.all()
    for tweet in tweets:
        was_updated = tweet.fetch()
        if was_updated:
            jug.publish('tweet-channel', tweet.__dict__)

def populate_redis():
    # pull this from config
    twitter_usernames = ('mindsnacks', 'mindsnacksfood')
    for username in twitter_usernames:
        TwitterItem(username)

@app.route('/')
def sonar():
    populate_redis()
    return render_template('index.html')

@app.route('/twitter-items')
def twitter_items():
    tweets = TwitterItem.all()
    tweets = [tweet.__dict__ for tweet in tweets]
    return jsonify(twitter_items=tweets)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
