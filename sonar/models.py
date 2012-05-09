"""
"""
from redis import Redis


class Item(object):
    _redis = Redis()

    def __init__(self, ident, object_id=None):
        self.name = self.__class__.__name__
        self.ident = ident
        self.object_id = object_id
        self.redis_key = self.make_key(self.name, self.ident)
        Item._redis.sadd(self.name, self.ident)

    @classmethod
    def all(cls):
        identifiers = cls._redis.smembers(cls.__name__)
        return [cls.get(ident) for ident in identifiers]

    @classmethod
    def get(cls, ident):
        item = cls(ident)
        item.update()
        return item

    @classmethod
    def exists(cls, item):
        pass

    def make_key(self, *args):
        """
        Creates a redis key from a list

        Format is:
        ClassName:identifier:attribute
        """
        return str.join(':', args)

    def update(self):
        """
        Update all of the attributes from redis.
        """
        unsafe_attrs = set(('redis_key', 'ident', 'name'))
        for attr, value in self.__dict__.iteritems():
            if attr not in unsafe_attrs:
                key = self.make_key(self.redis_key, attr)
                self.__dict__[attr] = Item._redis.get(key)

    def save(self):
        """
        Save all of the attributes to redis
        """
        Item._redis.set(self.redis_key, self.object_id)
        for attr, value in self.__dict__.iteritems():
            key = self.make_key(self.redis_key, attr)
            Item._redis.set(key, value)

    def delete(self):
        """
        Delete this object from redis
        """
        Item._redis.delete(self.redis_key)
        for attr in self.__dict__.keys():
            key = self.make_key(self.redis_key, attr)
            Item._redis.delete(key)

    def exists_in(self, redis):
        return Item._redis.get(self.redis_key) is not None

class TwitterItem(Item):

    from twitter import api
    _api = api.Twitter()

    def __init__(self, username, tweet_id=None, image_url='', text=''):
        self.image_url = image_url
        self.text = text
        super(TwitterItem, self).__init__(username, tweet_id)

    def fetch(self):
        was_updated = False

        last_tweet = TwitterItem._api.statuses.user_timeline(
                screen_name=self.ident,
                count=1,
                include_rts=False)
        if len(last_tweet) > 0:
            last_tweet = last_tweet[-1]
            last_tweet_id = str(last_tweet['id'])
            if last_tweet_id != self.object_id:
                self.object_id = last_tweet_id
                self.image_url = last_tweet['user']['profile_image_url']
                self.text = last_tweet['text']
                self.save()
                was_updated = True
        return was_updated
