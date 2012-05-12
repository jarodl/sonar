"""
"""
import base

class Instagram(object):
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

class InstagramSubscription(base.BaseItem):
    
    def __init__(self, object_type):
        """
        """
        self.object_type = object_type
        
    def fetch():
        pass

class InstagramPhoto(base.BaseItem):
    
    def __init__(self, location):
        """
        """
        self.location = location
        self.image_url = None
        super(InstagramPhoto, self).__init__(location)
        
    def fetch():
        pass