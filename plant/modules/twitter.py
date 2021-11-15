"""
Module to wrap tweepy functions.
"""

import os
import logging
import tweepy


class Twitter():

    def __init__(self):
        self.consumer_key = os.environ.get("CONSUMER_KEY", None)
        self.consumer_secret = os.environ.get("CONSUMER_SECRET", None)
        self.access_token = os.environ.get("ACCESS_TOKEN", None)
        self.access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET", None)

        assert self.consumer_key is not None
        assert self.consumer_secret is not None
        assert self.access_token is not None
        assert self.access_token_secret is not None

        self.api = self.get_api()

    def get_api(self):
        logging.info("Connecting to Twitter")
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return tweepy.API(auth)

    def tweet(self, tweet):
        logging.info("Tweeting: %s", tweet)
        self.api.update_status(status=tweet)
