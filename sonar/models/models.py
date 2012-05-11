"""
"""
import base

class TwitterItem(base.BaseItem):

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
