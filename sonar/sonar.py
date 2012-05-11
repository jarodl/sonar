import os
import json

from flask import Flask, jsonify
from flask import render_template, redirect, url_for, request
from flask.ext.celery import Celery

from gevent.pywsgi import WSGIServer
from juggernaut import Juggernaut

from models.models import LatestTweet

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
    tweets = LatestTweet.all()
    for tweet in tweets:
        was_updated = tweet.fetch()
        if was_updated:
            jug.publish('tweet-channel', tweet.__dict__)

def populate_redis():
    # pull this from config
    twitter_usernames = ('mindsnacks', 'mindsnacksfood', 'jarodltest')
    for username in twitter_usernames:
        tweet = LatestTweet(username)
        tweet.fetch()
        tweet.save()

@app.route('/')
def sonar():
    populate_redis()
    return render_template('index.html')

@app.route('/twitter/latest.json')
def latest_tweets():
    tweets = LatestTweet.all()
    tweets = [tweet.__dict__ for tweet in tweets]
    return jsonify(latest_tweets=tweets)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
