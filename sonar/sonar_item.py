"""
"""

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
