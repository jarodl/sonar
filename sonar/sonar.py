import os
import json
from flask import Flask, g, session, jsonify
from flask import render_template, redirect, url_for, request
from flask.ext.celery import Celery
from gevent.pywsgi import WSGIServer
from juggernaut import Juggernaut
from twitter import api
from redis import Redis

def create_app():
    return Flask(__name__)

app = create_app()
app.debug = True
app.config.from_pyfile("config.py")

jug = Juggernaut()
celery = Celery(app)
redis = Redis()

class Item(object):
    def __init__(self, ident, object_id=None):
        self.name = self.__class__.__name__
        self.ident = ident
        self.object_id = object_id
        self.redis_key = self.make_key(self.name, self.ident)

    def make_key(self, *args):
        """
        Creates a redis key from a list

        Format is:
        ClassName:identifier:attribute
        """
        return str.join(':', args)

    def update(self, redis):
        """
        Update all of the attributes from redis.
        """
        for attr, value in self.__dict__.iteritems():
            key = self.make_key(self.redis_key, attr)
            self.__dict__[attr] = redis.get(key)

    def save(self, redis):
        """
        Save all of the attributes to redis
        """
        redis.set(self.redis_key, self.object_id)
        for attr, value in self.__dict__.iteritems():
            key = self.make_key(self.redis_key, attr)
            redis.set(key, value)

    def delete(self, redis):
        """
        Delete this object from redis
        """
        redis.delete(self.redis_key)
        for attr in self.__dict__.keys():
            key = self.make_key(self.redis_key, attr)
            redis.delete(key)

    def exists_in(self, redis):
        return redis.get(self.redis_key) is not None

class TwitterItem(Item):

    def __init__(self, username, tweet_id=None, image_url='', text=''):
        self.image_url = image_url
        self.text = text
        super(TwitterItem, self).__init__(username, tweet_id)

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
