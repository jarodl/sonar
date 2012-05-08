import os
import json
from flask import Flask, g, session, jsonify
from flask import render_template, redirect, url_for, request
from flask.ext.celery import Celery
from gevent.pywsgi import WSGIServer
from juggernaut import Juggernaut
from twitter import api
from redis import Redis

from sonar_item import TwitterItem

def create_app():
    return Flask(__name__)

app = create_app()
app.debug = True
app.config.from_pyfile("config.py")

jug = Juggernaut()
celery = Celery(app)
redis = Redis()

def last_tweet_by(username):
    twitter = api.Twitter()
    last_tweet = twitter.statuses.user_timeline(
            screen_name=username,
            count=1,
            include_rts=False)
    last_tweet = last_tweet[-1]
    return last_tweet

@celery.task(name="sonar.update")
def update():
    update_tweets()

def update_tweets():
    twitter_usernames = redis.smembers('twitter_usernames')
    for username in twitter_usernames:
        last_tweet = last_tweet_by(username)
        # last_tweet = {
        #         'id': '123123123',
        #         'user' : {'profile_image_url': 'http://test.com/home.png'},
        #         'text': 'This is a test'
        #         };
        tweet = TwitterItem(
                username,
                str(last_tweet['id']),
                last_tweet['user']['profile_image_url'],
                last_tweet['text']
                )
        # last tweet is new
        if tweet.exists_in(redis) is False:
            old_tweet = TwitterItem(username)
            if old_tweet.exists_in(redis):
                old_tweet.update(redis)
                # notify client that tweet replaced old_tweet
                # old_tweet.delete(redis)
                jug.publish('tweet-channel', tweet.text)
            else:
                # just notify client tweet has been added
                jug.publish('tweet-channel', tweet.text)
            tweet.save(redis)
        jug.publish('tweet-channel', tweet.__dict__)

def populate_redis():
    # pull this from config
    twitter_usernames = ('mindsnacks', 'mindsnacksfood')
    for username in twitter_usernames:
        redis.sadd('twitter_usernames', username)

@app.route('/')
def sonar():
    populate_redis()
    return render_template('index.html')

@app.route('/twitter-items')
def twitter_items():
    twitter_usernames = redis.smembers('twitter_usernames')
    tweets = []
    for username in twitter_usernames:
        tweet = TwitterItem(username)
        tweet.update(redis)
        tweets.append(tweet)
    tweets = [tweet.__dict__ for tweet in tweets]
    return jsonify(twitter_items=tweets)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
