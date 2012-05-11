from redis import Redis

class BaseItem(object):
    _redis = Redis()

    def __init__(self, ident, object_id=None):
        self.name = self.__class__.__name__
        self.ident = ident
        self.object_id = object_id
        self.redis_key = self.make_key(self.name, self.ident)

    @classmethod
    def all(cls):
        identifiers = cls._redis.smembers(cls.__name__)
        return [cls.get(ident) for ident in identifiers]

    @classmethod
    def clear(cls):
        all_items = cls.all()
        for item in all_items:
            item.delete()

    @classmethod
    def get(cls, ident):
        item = cls(ident)
        if cls.exists(item):
            item.update()
            return item
        else:
            return None

    @classmethod
    def exists(cls, item):
        return cls._redis.get(item.redis_key) is not None

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
                self.__dict__[attr] = BaseItem._redis.get(key)

    def save(self):
        """
        Save all of the attributes to redis
        """
        BaseItem._redis.set(self.redis_key, self.object_id)
        BaseItem._redis.sadd(self.name, self.ident)
        for attr, value in self.__dict__.iteritems():
            key = self.make_key(self.redis_key, attr)
            BaseItem._redis.set(key, value)

    def delete(self):
        """
        Delete this object from redis
        """
        BaseItem._redis.delete(self.redis_key)
        BaseItem._redis.srem(self.name, self.ident)
        for attr in self.__dict__.keys():
            key = self.make_key(self.redis_key, attr)
            BaseItem._redis.delete(key)
